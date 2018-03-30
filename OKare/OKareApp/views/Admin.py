from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template import loader
from django.db.models import Count, Avg, Sum
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.http import Http404
from django.urls import reverse
from django.views import generic
from OKareApp.models import *
from datetime import timedelta, date, datetime, time
import calendar
import json
from django.core import serializers
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password, check_password
from django.views.generic.list import ListView
from django.db.models import F

from django.db.models import OuterRef, Subquery


def is_admin(user):
    return user.account.type == "Admin"

@login_required
@user_passes_test(is_admin)
# Create your views here.
def index(Request):
    #Id will get from session once login completed
    id = 1
    activeNurses = Account.objects.filter(type="Nurse").count()
    patients = Patient.objects.count()
    completed = CompletedTask.objects.filter(date = datetime.now().date()).count()
    today = datetime.now().date()
    helpRequest = HelpRequest.objects.filter(helper_id__isnull=True)

    remaining = Task.objects.filter(start_time__gte = datetime.now()).exclude(recur_type = "Monthly", date__day__lt = today.day, date__day__gt = today.day).exclude(recur_type = "Weekly", day__iexact = today.weekday()).exclude(id__in = OngoingTask.objects.all().values_list('task__id', flat=True)).count()

    # Team Productivity Report
    teamTaskAverages = {}

    #Store the Average of each team in dict
    for team in Teams.objects.all():
        teamTaskAverages[team.id] = \
            CompletedTask.objects.filter(nurse_id__team_id=team.id, date__month=((today.month - 1) % 13)).values(
                'nurse').annotate(total=Count(id)).aggregate(avg=Avg('total'))['avg']

    #Create dict
    nurseTotals = CompletedTask.objects.filter(date__month=((today.month - 1) % 13)).values('nurse','nurse__team_id','nurse__team__name').annotate(total=Count('id')).order_by('nurse')

    lowNurse = []
    for obj in nurseTotals:
        if obj['total'] < (teamTaskAverages[obj['nurse__team_id']]*0.9):
            lowNurse.append({'nric':obj['nurse'],
                             'name': Account.objects.get(nric=obj['nurse']).fullname(),
                             'total':obj['total'],
                             'team': obj['nurse__team__name']
                             })
    print(lowNurse)
    context = {
        'id': id,
        'activeNurses': activeNurses,
        'patients': patients,
        'completed': completed,
        'remaining': remaining,
        'ongoingTasks': OngoingTask.objects.all(),
        'helpRequest': helpRequest,
        'lowNurse': lowNurse
    }
    return render(Request, 'administrator/index.html', context)
pass

@login_required
@user_passes_test(is_admin)
#Used to Get Number of OutStanding Tasks in each Category
def getCatData(Request):
    today = datetime.now().date()
    categories = Task.objects.filter(start_time__gte=datetime.now()) \
        .exclude(recur_type="Monthly",date__day__lt=today.day,date__day__gt=today.day) \
        .exclude(recur_type="Weekly", day__iexact=today.weekday()) \
        .exclude(id__in=OngoingTask.objects.all().values_list('task__id', flat=True)) \
        .values('category') \
        .annotate(total=Count('category')).order_by('category')
    data = []
    for cat in categories:
        data.append({
            'category':cat['category'],
            'total':cat['total']
        })

    return JsonResponse(data, safe=False)
pass

@login_required
@user_passes_test(is_admin)
def managetask(Request):
    patients = Patient.objects.all
    context = {
        'Patients': patients
    }
    return render(Request, 'administrator/manage_task.html', context)

@login_required
@user_passes_test(is_admin)
def getPatientTasks(Request):
    id = Request.POST.get('id')
    context = {
        "tasks":Task.objects.filter(patient_id = id),
        "patient": Patient.objects.get(nric = id)
    }
    return render(Request, 'administrator/ui_components/task_panel.html', context)
    pass

@login_required
@user_passes_test(is_admin)
def manageteam(Request):
    all_teams = Teams.objects.all()
    context = {
        'teams': all_teams
    }

    # return HttpResponse(leads_as_json, content_type='json')
    return render(Request, 'administrator/manageteam.html', context)
pass

@login_required
@user_passes_test(is_admin)
def returnTeamInfo(Request):
    crisis_id = Request.POST.get("name")
    # getAgency = Crisis.objects.get(id = crisis_id)
    response_data = {}
    # if(getAgency.external_agencies is not None or getAgency.external_agencies != ""):
    #    response_data['agency'] = getAgency.external_agencies
    # else:
    #    response_data['agency'] = '';
    response_data['name'] = crisis_id;
    return JsonResponse(response_data)
pass

@login_required
@user_passes_test(is_admin)
def listPatients(Request):
    patients = Patient.objects.all()
    context = {
        'patients': patients,
        'updateTime': datetime.now().time()
    }
    return render(Request, 'administrator/list_patient.html', context)
pass

@login_required
@user_passes_test(is_admin)
def viewPatientProfile(Request, patient_id):
    patient = Patient.objects.filter(nric=patient_id).get()
    page_name = str(patient_id) + ": " + patient.first_name + " " + patient.last_name
    context = {
        'page_name': page_name,
        'patient_id': patient_id,
        'patient': patient,
    }
    return render(Request, 'administrator/view_patient.html', context)

@login_required
@user_passes_test(is_admin)
def addTask(Request):
    try:
        nric = Request.POST.get('Nric');
        title = Request.POST.get('Title');
        desctiption = Request.POST.get('Description');
        category = Request.POST.get('Category');
        recurType = Request.POST.get('RecurType');
        start_Time = Request.POST.get('Start_Time');
        hours = Request.POST.get('Hours');
        min = Request.POST.get('Minutes');
        date = Request.POST.get('Date');
        day = Request.POST.get('Day');
        duration = timedelta(hours=int(hours),minutes=int(min))
        patient = Patient.objects.get(nric=nric);
    except(KeyError):
        return JsonResponse({"success": False, "error": "Error Occurred Problems check key names!"})
    else:
        task = Task()
        task.patient = patient
        task.title = title
        task.description = desctiption
        task.category = category
        if recurType != '':
            task.recur_type = recurType
        task.start_time = datetime.strptime(start_Time, '%H:%M %p')
        task.date = datetime.strptime(date, '%d/%m/%Y')
        print(day)
        task.day = day
        task.duration = duration

        task.save()
        return JsonResponse({"success": True})

@login_required
@user_passes_test(is_admin)
def editTask(Request):
    try:
        title = Request.POST.get('Title');
        desctiption = Request.POST.get('Description');
        category = Request.POST.get('Category');
        recurType = Request.POST.get('RecurType');
        start_Time = Request.POST.get('Start_Time');
        hours = Request.POST.get('Hours');
        min = Request.POST.get('Minutes');
        date = Request.POST.get('Date');
        day = Request.POST.get('Day');
        duration = timedelta(hours=int(hours),minutes=int(min))
        id = Request.POST.get('Id')
    except(KeyError):
        return JsonResponse({"success": False, "error": "Error Occurred Problems check key names!"})
    else:
        task = Task.objects.get(id=id)
        task.title = title
        task.description = desctiption
        task.category = category
        if recurType != '':
            task.recur_type = recurType
        task.start_time = datetime.strptime(start_Time, '%H:%M %p')
        task.date = datetime.strptime(date, '%d/%m/%Y')
        task.day = day
        task.duration = duration

        task.save()

        return JsonResponse({"success": True})

@login_required
@user_passes_test(is_admin)
def getTask(Request, id):
    task = Task.objects.get(id=id)
    duration = task.duration
    hours = duration.total_seconds() // 3600
    minutes = (duration.total_seconds() % 3600) // 60

    data = {
        'id':task.id,
        'title': task.title,
        'description': task.description,
        'recur_type': task.recur_type,
        'category': task.category,
        'start_time': task.start_time.strftime('%H:%M %p'),
        'date': task.date.strftime('%d/%m/%Y'),
        'hours': hours,
        'minutes':minutes,
        'day': task.day
    }

    return JsonResponse(data,safe=False)

@login_required
@user_passes_test(is_admin)
def deleteTask(Request, id):
    try:
        task = Task.objects.get(id=id)
    except(KeyError):
        return JsonResponse({"success": False, "error": "Error Occurred Problems check key names!"})
    else:
        task.delete()
        return JsonResponse({"success": True})

@login_required
@user_passes_test(is_admin)
def getNurseTeammates(Request, id):
    print(id)
    nurse = Account.objects.get(nric=id)
    teammates = Account.objects.filter(team = nurse.team).exclude(nric=id)

    data = []
    for mate in teammates:
        data.append({'id':mate.nric,
                     'name':mate.fullname()
                     })

    return JsonResponse(data, safe=False)

@login_required
@user_passes_test(is_admin)
def assignNurseHr(Request):
    try:
        id = Request.POST.get('Id')
        nric = Request.POST.get('Nurse')
    except(KeyError):
        return JsonResponse({"success": False, "error": "Error Occurred! Check ID and NRIC"})
    else:
        helpRequest = HelpRequest.objects.get(id=id)
        helpRequest.helper = Account.objects.get(nric=nric)
        helpRequest.save()
        #notify requester and helper
        notification_bell = NotificationBell(type="Assignment", target=helpRequest.helper, title="You have been Assigned to help "+str(helpRequest.requester)+"! Please Proceed to help your teammates!", helpRequest=helpRequest)
        notification_bell.save()
        notification_bell2 = NotificationBell(type="Response", target=helpRequest.requester,title="Your request was accepted")
        notification_bell2.save()
        return JsonResponse({"success": True})
@login_required
@user_passes_test(is_admin)
def listNurses(request):
    template = loader.get_template('administrator/list_nurse.html')
    page_name = 'View Nurse'    #Fill in here

    nurses = Account.objects.filter(type="Nurse")
    #user session havn't implement yet, so placeholder
    user_name="Benjamin"
    user_type="Nurse"
    context = {
        'page_name': page_name,
        'user_name': user_name,
        'user_type': user_type,
        'nurses': nurses,
    }
    return HttpResponse(template.render(context, request))


@login_required
@user_passes_test(is_admin)
def viewNurseProfile(request, nurse_id):
    template = loader.get_template('administrator/view_nurse.html')
    nurse = Account.objects.filter(user_id=nurse_id).get()
    nurse.date_of_birth = nurse.date_of_birth.strftime('%d/%m/%Y')
    nurse_name = nurse.user.first_name + " " + nurse.user.last_name    # From Models

    page_name = str(nurse.user_id) + ": " + nurse_name  # Fill in here
    context = {
        'page_name': page_name,
        'nurse': nurse,
    }
    return HttpResponse(template.render(context, request))


@login_required
@user_passes_test(is_admin)
def addNurseView(request):
    template = loader.get_template('administrator/add_nurse.html')


    #assignTask()
    # lmaotest()

    lmao = CompletedTask.objects.filter(task_id='29')
    for i in lmao:
        print(i.compldt)

    context = {
        'page_name': "Add Nurse",
    }
    return HttpResponse(template.render(context, request))


@login_required
@user_passes_test(is_admin)
def addNurse(request):
    if request.POST:
        print(request.POST)
        #alidate nric
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        nric = request.POST['nric']
        date_of_birth = request.POST['date_of_birth']
        street = request.POST['street']
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip_code']
        phone_no = request.POST['phone_no']
        user_name = request.POST['user_name']
        pass_word = request.POST['pass_word']
        email = request.POST['email']

        converted_datetime = datetime.strptime(date_of_birth, "%d/%m/%Y")

        if Account.objects.filter(nric=nric).exists():
            return HttpResponse('duplicated_nric')
        else:
            if User.objects.filter(username=user_name).exists():
                return HttpResponse('duplicated_username')
            else:
                user = User.objects.create_user(username=user_name,
                                                email=email,
                                                password=pass_word,
                                                first_name=first_name,
                                                last_name=last_name)

                addeduser = User.objects.filter(username=user_name).get()

                nurse = Account(nric=nric, date_of_birth=converted_datetime,
                                street=street, city=city, state=state, zip_code=zip_code, phoneNo=phone_no, type="Nurse",
                                team_id=1,user_id=addeduser.id)

                nurse.save()
                return HttpResponse('successful')


@login_required
@user_passes_test(is_admin)
def updateNurseDetail(request):
    if request.POST:
        try:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']

            nric = request.POST['nric']
            date_of_birth = request.POST['date_of_birth']
            street = request.POST['street']
            city = request.POST['city']
            state = request.POST['state']
            zip_code = request.POST['zip_code']
            phone_no = request.POST['phone_no']

            # user_name = request.POST['user_name']
            pass_word = request.POST['pass_word']
            email = request.POST['email']

            converted_datetime = datetime.datetime.strptime(date_of_birth, "%d/%m/%Y")

            nurse = Account.objects.get(nric=nric)

            user = nurse.user
            user.first_name = first_name
            user.last_name = last_name

            # nurse.nric = nric
            nurse.date_of_birth = converted_datetime
            nurse.street = street
            nurse.city = city
            nurse.state = state
            nurse.zip_code = zip_code
            nurse.phoneNo = phone_no

            user.password = make_password(pass_word)
            user.email = email

            nurse.save()
            user.save()

        except(KeyError, Account.DoesNotExist):
            return HttpResponse('unsuccessful')

        else:
            return HttpResponse('successful')


@login_required
@user_passes_test(is_admin)
def listPatients(request):
    template = loader.get_template('administrator/list_patient.html')
    page_name = 'View Patient'    #Fill in here

    patients = Patient.objects.all()

    context = {
        'page_name': page_name,
        'patients': patients,
    }
    return HttpResponse(template.render(context, request))


@login_required
@user_passes_test(is_admin)
def viewPatientProfile(request, patient_id):
    template = loader.get_template('administrator/view_patient.html')
    patient = Patient.objects.filter(nric=patient_id).get()
    patient.date_of_birth = patient.date_of_birth.strftime('%d/%m/%Y')
    page_name = str(patient_id) + ": " + patient.first_name + " " + patient.last_name

    context = {
        'page_name': page_name,
        'patient_id': patient_id,
        'patient': patient,
    }
    return HttpResponse(template.render(context, request))


@login_required
@user_passes_test(is_admin)
def addPatientView(request):
    template = loader.get_template('administrator/add_patient.html')
    context = {
        'page_name': "Add Patient",
    }
    return HttpResponse(template.render(context, request))


@login_required
@user_passes_test(is_admin)
def addPatient(request):
    if request.POST:
        nric = request.POST['nric']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        date_of_birth = request.POST['date_of_birth']
        ward = request.POST['ward']
        bed = request.POST['bed']
        street = request.POST['street']
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip_code']
        phone_no = request.POST['phone_no']

        converted_datetime = datetime.strptime(date_of_birth, "%d/%m/%Y")

        if Patient.objects.filter(nric=nric).exists():
            return HttpResponse('duplicated_nric')
        else:
            if Patient.objects.filter(bed=bed, ward=ward).exists():
                return HttpResponse('duplicated_bed')
            else:
                patient = Patient.objects.create(nric=nric, first_name=first_name, last_name=last_name,
                                                 date_of_birth=converted_datetime, ward=ward, bed=bed, street=street,
                                                 city=city, state=state, zip_code=zip_code, phoneNo=phone_no)

                patient.save()
                return HttpResponse('successful')


@login_required
@user_passes_test(is_admin)
def updatePatientDetail(request):
    if request.POST:
        try:
            nric = request.POST['nric']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            date_of_birth = request.POST['date_of_birth']
            ward = request.POST['ward']
            bed = request.POST['bed']
            street = request.POST['street']
            city = request.POST['city']
            state = request.POST['state']
            zip_code = request.POST['zip_code']
            phone_no = request.POST['phone_no']

            patient = Patient.objects.get(nric=nric)

            #Format date..
            converted_datetime = datetime.datetime.strptime(date_of_birth, "%d/%m/%Y")

            # patient.nric = nric
            patient.first_name = first_name
            patient.last_name = last_name
            patient.date_of_birth = converted_datetime
            patient.ward = ward
            patient.bed = bed
            patient.street = street
            patient.city = city
            patient.state = state
            patient.zip_code = zip_code
            patient.phoneNo = phone_no

            patient.save()

        except(KeyError, Patient.DoesNotExist):
            return HttpResponse('unsuccessful')

        else:
            return HttpResponse('successful')


@login_required
@user_passes_test(is_admin)
def generateProductivityReport(request, nurse_id):
    template = loader.get_template('administrator/productivity_report.html')

    nurse = Account.objects.filter(user_id=nurse_id).get()
    tasks = CompletedTask.objects.filter(nurse_id=nurse.nric)

    allNurses = Account.objects.filter(team_id=nurse.team_id)
    allTasks = CompletedTask.objects.filter(nurse_id__in=allNurses).exclude(nurse_id=nurse.nric)

    #Tasks/Day for Nurse vs Average of Team

    curMonth = datetime.today().month
    if curMonth==1:
        prevMonth = 12
    else:
        prevMonth = curMonth -1
    print(prevMonth)
    print(calendar.monthrange(datetime.today().year, prevMonth)[1])

    graphData = []

    cal = calendar.Calendar()
    for n in cal.itermonthdays(datetime.today().year, curMonth):
        if n != 0:
            curDate = date(year=datetime.today().year, month=curMonth, day=n)

            complTasks = CompletedTask.objects.filter(nurse_id=nurse.nric, date=curDate).count()
            avg_tasks_today = CompletedTask.objects.filter(nurse_id__in=allNurses, date=curDate).exclude(nurse_id=nurse.nric).count()/(allNurses.count()-1)

            print(str(curDate) + "- NurseTasks: " + str(complTasks) + ", AvgTeamTasks: " + str(avg_tasks_today) + ", TeamNurses: " + str(allNurses.count()-1))

            graphObj = {
                "date": str(curDate),
                "tasks_completed": complTasks,
                "avg_tasks_completed": avg_tasks_today
            }

            graphData.append(graphObj)

    page_name = 'Generate Productivity Report: ' + nurse_id + " (" + nurse.user.first_name + ")"
    context = {
        'page_name': page_name,
        'nurse_id': nurse_id,
        'nurse': nurse,
        'tasks': tasks,
        'graphData': json.dumps(graphData), #For Tasks Completed vs Team avg
    }
    return HttpResponse(template.render(context, request))

def generateProductivityReport2(request, nurse_id):
    template = loader.get_template('nurse/productivity_report.html')

    nurse = Account.objects.filter(user_id=nurse_id).get()
    tasks = CompletedTask.objects.filter(nurse_id=nurse.nric)

    allNurses = Account.objects.filter(team_id=nurse.team_id)
    allTasks = CompletedTask.objects.filter(nurse_id__in=allNurses).exclude(nurse_id=nurse.nric)

    numNurses = 0
    for b in allNurses:
        numNurses += 1

    #Compute values for graph here:

    #1. Tasks/month for a quarter (4 mths)

    today = datetime.today()
    graph1data = []
    graph2data = []

    # ONE WEEK
    for i in range(0,7):
        curDate = today-timedelta(days=i)

        complTasks = 0
        #totalDur = datetime.timedelta(0,0,0)
        totalDur = 0 #in Mins

        allComplTasks = 0
        avg_tasks_today = 0

        #allTotalDur = datetime.timedelta(0,0,0)
        allTotalDur = 0 #in Mins

        #Average Tasks: (Tasks not done by THIS NURSE / Nurses in the team -1)
        for a in allTasks:
            if a.date == curDate.date():

                #days = a.duration.days
                #hours = a.duration.seconds // 3600
                mins = a.duration.seconds % 3600 / 60.0

                #print(days, hours, mins)
                allTotalDur += mins
                allComplTasks += 1

        if numNurses-1 > 0:
            avg_tasks_today = allComplTasks/(numNurses-1)
        else:
            avg_tasks_today = 0

        if allComplTasks > 0:
            avg_duration_today = allTotalDur/allComplTasks
        else:
            avg_duration_today = timedelta(0,0,0)

        #Get number of tasks completed by THIS NURSE in the current month
        for t in tasks:
            if t.date == curDate.date():
                #totalDur += t.duration
                #print(tDur)
                #print(testDur)

                #days = t.duration.days
                #hours = t.duration.seconds // 3600.0
                mins2 = t.duration.seconds % 3600 / 60.0

                #print(days, hours, mins)

                totalDur += mins2

                complTasks += 1

        if complTasks > 0:
            avgDur = totalDur/complTasks
        else:
            avgDur = 0

        graph1dataObj = {
            "date": str(curDate.date()),
            "tasks_completed": complTasks,
            "avg_tasks_completed": avg_tasks_today
        }

        graph2DataObj = {
            "date": str(curDate.date()),
            "avg_duration": str(avgDur),
            "team_avg_duration": str(avg_duration_today)
        }

        graph2data.append(graph2DataObj)

        #2. Graph 2 - Average Duration/Task (Accumulated over time) over 7 days
        graph1data.append(graph1dataObj)

        print("end for loop here")

    #3. Graph 3 - Helps against average in team

    allHelps = NurseStats.objects.all() #Lol whatswith this model where de fkey

    page_name = 'Generate Productivity Report: ' + nurse_id + " (" + nurse.user.first_name + ")"
    context = {
        'page_name': page_name,
        'nurse_id': nurse_id,
        'nurse': nurse,
        'tasks': tasks,
        'graph1data': json.dumps(graph1data), #For Tasks Completed vs Team avg
        'graph2data': json.dumps(graph2data), #For Task Duration vs Team avg
    }
    return HttpResponse(template.render(context, request))



