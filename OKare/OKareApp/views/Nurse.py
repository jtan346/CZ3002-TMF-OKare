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

def viewNurseProfile(request, nurse_id):
    template = loader.get_template('nurse/view_nurse.html')
    nurse = Account.objects.filter(user_id=nurse_id).get()
    nurse_name = nurse.user.first_name + " " + nurse.user.last_name    # From Models

    page_name = str(nurse.user_id) + ": " + nurse_name  # Fill in here
    context = {
        'page_name': page_name,
        'nurse': nurse,
    }
    return HttpResponse(template.render(context, request))

def addNurseView(request):
    template = loader.get_template('nurse/add_nurse.html')
    context = {
                'page_name': "Adding a Nurse",
               }
    return HttpResponse(template.render(context, request))

def addNurse(request):
    if request.POST:
        print(request.POST)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        nric = request.POST['nric']
        date_of_birth = request.POST['date_of_birth']
        street = request.POST['street']
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip_code']
        phone_no = request.POST['phone_no']

        nurse = Account(nric=nric, first_name=first_name, last_name=last_name, date_of_birth=date_of_birth,
                        street=street, city=city, state=state, zip_code=zip_code, phoneNo=phone_no, type="",
                        team_id=1)

        nurse.save()

        return HttpResponse('successful')

def updateNurseDetail(request):
    if request.POST:
        try:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']

            nric = request.POST['nric']
            # date_of_birth = request.POST['date_of_birth']
            street = request.POST['street']
            city = request.POST['city']
            state = request.POST['state']
            zip_code = request.POST['zip_code']
            phone_no = request.POST['phone_no']

            nurse = Account.objects.get(nric=nric)

            user = nurse.user
            user.first_name = first_name
            user.last_name = last_name

            # nurse.nric = nric
            # nurse.date_of_birth = date_of_birth
            nurse.street = street
            nurse.city = city
            nurse.state = state
            nurse.zip_code = zip_code
            nurse.phoneNo = phone_no

            nurse.save()
            user.save()

        except(KeyError, Account.DoesNotExist):
            return HttpResponse('unsuccessful')

        else:
            return HttpResponse('successful')

def listPatients(request):
    template = loader.get_template('nurse/list_patient.html')
    page_name = 'View Patient'    #Fill in here

    patients = Patient.objects.all()

    context = {
        'page_name': page_name,
        'patients': patients,
    }
    return HttpResponse(template.render(context, request))

def viewPatientProfile(request, patient_id):
    template = loader.get_template('nurse/view_patient.html')
    patient = Patient.objects.filter(nric=patient_id).get()
    page_name = str(patient_id) + ": " + patient.first_name + " " + patient.last_name

    context = {
                'page_name': page_name,
                'patient_id': patient_id,
                'patient': patient,
               }
    return HttpResponse(template.render(context, request))

def addPatientView(request):
    template = loader.get_template('nurse/add_patient.html')
    context = {
                'page_name': "Adding a Patient",
               }
    return HttpResponse(template.render(context, request))

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

        patient = Patient(nric=nric, first_name=first_name, last_name=last_name, date_of_birth=date_of_birth,
                          ward=ward, bed=bed, street=street, city=city, state=state, zip_code=zip_code,
                          phoneNo=phone_no, team_id=1)

        patient.save()
        return HttpResponse('successful')

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
            datetimeobj = datetime.datetime.strptime(date_of_birth, "%B %d, %Y")

            # patient.nric = nric
            patient.first_name = first_name
            patient.last_name = last_name
            patient.date_of_birth = datetimeobj
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


def view_team_tasklist(request):
    #team is from nurse's team, retrieved from user, awaiting completion of login
    team = 1
    team_tasks = Task.object.fliter(patient__team__in=team)
    context = { "team_tasks": team_tasks }
    return render(request,'nurse/team_tasklist.html',context)

#ListView
class TeamTaskList(ListView):
    context_object_name="team_tasks"
    template_name = 'nurse/team_tasklist.html'
    #model=
    #queryset=

    def get_queryset(self):
        today = datetime.now().date()
        #first, filter start_time greater or equal to the current time - gets all tasks whose start time
        #then , exclude those task date's day is not before today's day and
        return Task.objects.filter(start_time__gte=datetime.now(), patient__team__in=[1]).exclude(~Q(date__day=datetime.now().day), Q(recur_type='Monthly') | Q(recur_type__isnull=True))

        #return Task.objects.filter(start_time__gte=datetime.now(), patient__team__in=[1]).exclude(recur_type="Monthly",date__day__lt=today.day,date__day__gt=today.day).exclude(recur_type="Weekly", day__iexact=today.weekday()).exclude(id__in=OngoingTask.objects.all().values_list('task__id', flat=True))
#       user = self.request.
#       return Tasks.object.filter(patient__team__in=self.)

def index(request):
    #assigned_task = OngoingTask.objects.filter(nurse=request)[0]
    assigned_task = OngoingTask.objects.filter(nurse=Account.objects.get(nric="S9232342G")).first()
    context = { 'assigned_task':assigned_task }
    return render(request,'nurse/index.html', context)

def add_help_request(request):
    if request.method == "POST":
        try:
            account = get_object_or_404(Account, nric="S9232342G")
            task = OngoingTask.objects.get(nurse=account).task
            help_request = HelpRequest(requester=account, helper=None, task=task)
            # help_request.save()
        except(KeyError, Account.DoesNotExist):
            return HttpResponse("Failure")
        else:
            return HttpResponse("Success")

def list_help_request(request):
    account = get_object_or_404(Account, nric="S9232342G")
    help_requests = HelpRequest.objects.filter(Q(requester__team=account.team) & ~Q(requester=account))
    context = { 'help_requests' : help_requests }
    return JsonResponse(context)

def check_help_request(request):
    pass



