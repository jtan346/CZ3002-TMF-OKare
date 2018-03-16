from django.shortcuts import render
from django.db.models import Count, Avg, Sum
from OKareApp.models import Account,Task, CompletedTask, DailyTriage,Patient,NurseStats, OngoingTask, Teams
from datetime import datetime, timedelta

# Create your views here.
def index(Request):
    #Id will get from session once login completed
    id = 1
    activeNurses = Account.objects.filter(type="Nurse")
    patients = Patient.total_patients
    completed = CompletedTask.total_tasks_completed
    remaining = 0#Task.total_remaining_tasks_for_day(datetime.now)
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

def manageteam(Request):
    all_teams = Teams.objects.all()
    context = {
        'teams': all_teams
    }

    # return HttpResponse(leads_as_json, content_type='json')
    return render(Request, 'administrator/manageteam.html', context)
    pass


def getCatData(Request):
    tasks = Task.objects.exclude(id = OngoingTask.id).exclude(id = CompletedTask)



def returnTeamInfo(Request):
    crisis_id = request.POST.get("name")
    # getAgency = Crisis.objects.get(id = crisis_id)
    response_data = {}
    # if(getAgency.external_agencies is not None or getAgency.external_agencies != ""):
    #    response_data['agency'] = getAgency.external_agencies
    # else:
    #    response_data['agency'] = '';
    response_data['name'] = crisis_id;
    return JsonResponse(response_data)