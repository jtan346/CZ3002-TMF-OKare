from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.db.models import Q
from OKareApp.models import *
import datetime
import time
from datetime import timedelta, date
import calendar
import json
from django.core import serializers
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password, check_password

def is_nurse(user):
    return user.account.type == "Nurse"

@login_required
@user_passes_test(is_nurse)
def listNurses(request):
    template = loader.get_template('nurse/list_nurse.html')
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
@user_passes_test(is_nurse)
def viewNurseProfile(request, nurse_id):
    template = loader.get_template('nurse/view_nurse.html')
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
@user_passes_test(is_nurse)
def addNurseView(request):
    template = loader.get_template('nurse/add_nurse.html')

    assignTask()
    # lmaotest()

    lmao = CompletedTask.objects.filter(task_id='29')
    for i in lmao:
        print(i.compldt)

    context = {
                'page_name': "Add Nurse",
               }
    return HttpResponse(template.render(context, request))

def assignTask():

    allCompleteTasks = CompletedTask.objects.all()

    #Get all tasks that are not completed/ongoing and need to be started (time < now)

    completeIds = []
    for i in allCompleteTasks:
        # print(i.compldt)
        # print(i.duration)
        endDate = i.compldt
        dur = i.duration
        intendedDate = endDate - dur + timedelta(hours=8)
        print(endDate)
        print(dur)
        print("ID:" + str(i.task_id) + " Start Date:" + str(intendedDate.strftime('%d')))
        if intendedDate.strftime('%d') == datetime.datetime.today().strftime('%d'):
            completeIds.append(i.task.id)

    print("Completed IDs: ")
    print(completeIds)
    toBeAssigned = Task.objects.exclude(id__in=OngoingTask.objects.all().values('task')).exclude(id__in=completeIds).filter(date=date.today()).order_by('start_time')

    #Emulate Task Queue

    taskQueue = []

    for a in toBeAssigned:
        print(a.id, a.start_time, datetime.datetime.now().time(), a.start_time < datetime.datetime.now().time())
        if a.start_time < datetime.datetime.now().time():
            taskQueue.append(a)

    #print(len(taskQueue))

    for i in taskQueue:
        #DO THE ASSIGNING GOD
        #GOD SAID LET THERE BE TASKS FOR YOU SLAVE
        #assign i to a nurse

        # Find free nurse(s) in team where patient is from:
        patient = Patient.objects.filter(nric=i.patient_id).get()

        # Requery every round because free nurses must be updated, just assign to first nurse in queryset if any
        freeNurses = Account.objects.exclude(nric__in=OngoingTask.objects.all().values('nurse_id')).filter(type='Nurse').filter(team_id=patient.team_id)
        #print(patient.team_id)

        #Only if got free nurses in team god
        if freeNurses:
            print("Free Nurse ID: " + str(freeNurses[0].nric))
            print("Task ID: " + str(i.id))
            ongoingtask = OngoingTask(assigned_datetime=datetime.datetime.now(), nurse_id=freeNurses[0].nric, task_id=i.id)
            ongoingtask.save()

    chek = OngoingTask.objects.all()
    for bla in chek:
        print(bla)

def lmaotest():
    #delete task 29 from ongoing and put into completed
    tasktodel = OngoingTask.objects.filter(task_id='29').get()
    print("HERE" + str(tasktodel.task_id))
    nownow = str(datetime.datetime.today())
    print(nownow) #wtf
    compltask = CompletedTask(duration=datetime.timedelta(minutes=30), date=datetime.date.today(), compldt=datetime.datetime.today(), nurse_id=tasktodel.nurse_id, task_id=tasktodel.task_id)
    compltask.save()
    tasktodel.delete()

@login_required
@user_passes_test(is_nurse)
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

        converted_datetime = datetime.datetime.strptime(date_of_birth, "%d/%m/%Y")

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
@user_passes_test(is_nurse)
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
@user_passes_test(is_nurse)
def listPatients(request):
    template = loader.get_template('nurse/list_patient.html')
    page_name = 'View Patient'    #Fill in here

    patients = Patient.objects.all()

    context = {
        'page_name': page_name,
        'patients': patients,
    }
    return HttpResponse(template.render(context, request))

@login_required
@user_passes_test(is_nurse)
def viewPatientProfile(request, patient_id):
    template = loader.get_template('nurse/view_patient.html')
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
@user_passes_test(is_nurse)
def addPatientView(request):
    template = loader.get_template('nurse/add_patient.html')
    context = {
                'page_name': "Add Patient",
               }
    return HttpResponse(template.render(context, request))

@login_required
@user_passes_test(is_nurse)
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

        converted_datetime = datetime.datetime.strptime(date_of_birth, "%d/%m/%Y")

        patient = Patient(nric=nric, first_name=first_name, last_name=last_name, date_of_birth=converted_datetime,
                          ward=ward, bed=bed, street=street, city=city, state=state, zip_code=zip_code,
                          phoneNo=phone_no, team_id=1)

        patient.save()
        return HttpResponse('successful')

@login_required
@user_passes_test(is_nurse)
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
@user_passes_test(is_nurse)
def generateProductivityReport(request, nurse_id):
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

    today = datetime.datetime.today()
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
            avg_duration_today = datetime.timedelta(0,0,0)

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

@login_required
@user_passes_test(is_nurse)
def view_team_tasklist(request):
    #team is from nurse's team, retrieved from user, awaiting completion of login
    team_tasks = Task.objects.filter(start_time__gte=datetime.datetime.now(), patient__team=request.user.account.team).exclude(~Q(date__day=datetime.datetime.now().day), Q(recur_type='Monthly') | Q(recur_type__isnull=True))
    context = { "team_tasks": team_tasks,
                'name': request.user.first_name,
                'usertype': request.user.account.type
                }
    return render(request,'nurse/team_tasklist.html',context)

@login_required
@user_passes_test(is_nurse)
def index(request):
    assigned_task = OngoingTask.objects.filter(nurse=request.user.account).first()
    context = { 'assigned_task':assigned_task,
                'name': request.user.first_name,
                'usertype': request.user.account.type}

    return render(request,'nurse/index.html', context)

@login_required
@user_passes_test(is_nurse)
def list_current_task(request):
    assigned_task = OngoingTask.objects.filter(nurse=request.user.account).first()
    context = { 'assigned_task':assigned_task }
    return render(request,'nurse/ui_components/current_task.html', context)

@login_required
@user_passes_test(is_nurse)
def complete_task(request):
    if request.method =="POST":
        try:
            assigned_task = OngoingTask.objects.filter(nurse=request.user.account).first()
            duration = datetime.datetime.now(datetime.timezone.utc) - assigned_task.assigned_datetime
            print(duration)
            completed_task = CompletedTask(task=assigned_task.task, date=assigned_task.task.date,
                                           nurse=assigned_task.nurse, duration=duration)
            completed_task.save()
            assigned_task.delete()
            #assignTask()
        except(Exception):
            return HttpResponse("FAILURE")
        else:
            return HttpResponse("SUCCESS")

@login_required
@user_passes_test(is_nurse)
def add_help_request(request):
    if request.method == "POST":
        try:
            account = request.user.account
            current_task = OngoingTask.objects.get(nurse=account)
            help_request = HelpRequest(requester=account, helper=None, task=current_task.task, ongoing_task=current_task)
            help_request.save()
        except(KeyError, Account.DoesNotExist):
            return HttpResponse("Failure")
        else:
            return HttpResponse("Success")

#list help requests lists all the help requests for a person to accept
@login_required
@user_passes_test(is_nurse)
def list_unread_help_request(request):
    assignTask()
    account = request.user.account
    help_requests = HelpRequest.objects.filter(Q(requester__team=account.team) & ~Q(requester=account), helper__isnull=True).exclude(
        id__in=Notification.objects.filter(reader=account, read_type="Help Requested").values('help_request'))

    print(help_requests)
    for help_request in help_requests:
        i_read_this = Notification(reader=account, help_request=help_request, read_type="Help Requested")
        i_read_this.save()

    context = { 'help_requests' : help_requests }
    # this gives you a list of dicts
    raw_data = serializers.serialize('python', help_requests)
    # now extract the inner `fields` dicts
    actual_data = [d['fields'] for d in raw_data]

    for request in actual_data:
        nric = request['requester']
        request['requester'] = Account.objects.get(nric=nric).fullname()
        del request['time_created']

    # and now dump to JSON
    return JsonResponse(actual_data,safe=False)

@login_required
@user_passes_test(is_nurse)
def list_allowed_help_requests(request):
    account = request.user.account
    allowed_help_requests = HelpRequest.objects.filter(Q(requester__team=account.team) & ~Q(requester=account), helper__isnull=True).\
        exclude(helper=account)

    try:
        ongoing_task = OngoingTask.objects.get(nurse=account)
        created_help_requests = HelpRequest.objects.filter(requester=account, ongoing_task=ongoing_task)
    except (OngoingTask.DoesNotExist):
        created_help_requests = None

    context = {
        'created_help_requests' : created_help_requests,
        'allowed_help_requests' : allowed_help_requests
    }

    return render(request, 'nurse/help_requests.html', context)

@login_required
@user_passes_test(is_nurse)
def reload_allowed_help_requests(request):
    account = request.user.account
    allowed_help_requests = HelpRequest.objects.filter(Q(requester__team=account.team) & ~Q(requester=account), helper__isnull=True).\
        exclude(ongoing_task__in=HelpRequest.objects.filter(helper=account).values('ongoing_task'))

    try:
        ongoing_task = OngoingTask.objects.get(nurse=account)
        created_help_requests = HelpRequest.objects.filter(requester=account, ongoing_task=ongoing_task)
    except (OngoingTask.DoesNotExist):
        created_help_requests = None

    context = {
        'created_help_requests' : created_help_requests,
        'allowed_help_requests' : allowed_help_requests
    }

    return render(request, 'nurse/ui_components/help_requests.html', context)

#check help request returns a list of help requests initiated by the account to see if they are acepted
@login_required
@user_passes_test(is_nurse)
def check_help_request(request):
    account = request.user.account
    try:
        ongoing_task = OngoingTask.objects.get(nurse=account)
        help_requests = HelpRequest.objects.filter(requester=account, acknowledgement=False, helper__isnull=False, ongoing_task=ongoing_task).\
            exclude(id__in=Notification.objects.filter(reader=account, read_type="Help Accepted").values('help_request'))

        for help_request in help_requests:
            i_read_this = Notification(reader=account, help_request=help_request, read_type="Help Accepted")
            i_read_this.save()

        # .update(acknowledgement=True)
        # this gives you a list of dicts
        raw_data = serializers.serialize('python', help_requests)
        # now extract the inner `fields` dicts
        actual_data = [d['fields'] for d in raw_data]

        for request in actual_data:
            nric = request['helper']
            request['helper'] = Account.objects.get(nric=nric).fullname()
            del request['time_created']
    except(Exception):
        actual_data = {}

    # and now dump to JSON
    return JsonResponse(actual_data,safe=False)

@login_required
@user_passes_test(is_nurse)
def accept_help_request(request):
    account = request.user.account
    help_request_id = request.POST.get("id")
    help_request = HelpRequest.objects.get(id=help_request_id)
    help_request.helper = account
    help_request.save()
    return HttpResponse("OKAY")

