from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template import loader
from django.db.models import Count, Avg, Sum
from OKareApp.models import Account,Task, CompletedTask, DailyTriage,Patient,NurseStats, OngoingTask, Teams
from datetime import datetime, timedelta
from django.db.models import Q

# Create your views here.
def index(Request):
    #Id will get from session once login completed
    id = 1
    activeNurses = Account.objects.filter(type="Nurse").count()
    patients = Patient.objects.count()
    completed = CompletedTask.objects.filter(date = datetime.now().date()).count()
    today = datetime.now().date()

    dayOfWeek ={
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }

    remaining = Task.objects.filter(start_time__gte = datetime.now()).exclude(recur_type = "Monthly", date__day__lt = today.day, date__day__gt = today.day).exclude(recur_type = "Weekly", day__iexact = dayOfWeek[today.weekday()]).exclude(id__in = OngoingTask.objects.all().values_list('task__id', flat=True)).count()

    ongoingTasks = OngoingTask.objects.all
    context = {
        'id': id,
        'activeNurses': activeNurses,
        'patients': patients,
        'completed': completed,
        'remaining': remaining,
        'ongoingTasks':ongoingTasks
    }
    return render(Request, 'administrator/index.html', context)
pass


#Used to Get Number of OutStanding Tasks in each Category
def getCatData(Request):
    tasks = Task.objects.exclude(id = OngoingTask.id).exclude(id = CompletedTask).values('cateogry').annotate(catCount=Count('category'))

    data = [tasks]

    return JsonResponse(data, safe=False)
pass


def managetask(Request):
    patients = Patient.objects.all
    context = {
        'Patients': patients
    }
    return render(Request, 'administrator/manage_task.html', context)

def getPatientTasks(Request):
    id = Request.POST.get('id')
    context = {
        "tasks":Task.objects.filter(patient_id = id),
        "patient": Patient.objects.get(nric = id)
    }
    return render(Request, 'administrator/ui_components/task_panel.html', context)
    pass


def manageteam(Request):
    all_teams = Teams.objects.all()
    context = {
        'teams': all_teams
    }

    # return HttpResponse(leads_as_json, content_type='json')
    return render(Request, 'administrator/manageteam.html', context)
pass


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


def listPatients(Request):
    patients = Patient.objects.all()
    context = {
        'patients': patients,
        'updateTime': datetime.now().time()
    }
    return render(Request, 'administrator/list_patient.html', context)
pass

def viewPatientProfile(Request, patient_id):
    patient = Patient.objects.filter(nric=patient_id).get()
    page_name = str(patient_id) + ": " + patient.first_name + " " + patient.last_name
    context = {
                'page_name': page_name,
                'patient_id': patient_id,
                'patient': patient,
               }
    return render(Request, 'administrator/view_patient.html', context)