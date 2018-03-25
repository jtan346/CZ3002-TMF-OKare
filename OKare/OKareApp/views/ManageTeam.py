from django.shortcuts import render
from OKareApp.models import Teams
from OKareApp.models import Patient
from OKareApp.models import Account
from django.http import JsonResponse
<<<<<<< Updated upstream
<<<<<<< Updated upstream
from django.core import serializers
=======
from django.http import HttpResponse
from django.template import loader

>>>>>>> Stashed changes
=======
from django.http import HttpResponse
from django.template import loader

>>>>>>> Stashed changes
import json


# Create your views here.
def index(request):

    all_teams = Teams.objects.all()
    context = {
        'teams': all_teams
    }

    # return HttpResponse(leads_as_json, content_type='json')
    return render(request, 'administrator/manageteam.html', context)
    pass


def removeteam(request):
    team_id = request.POST.get("teamid")
    print(team_id)
    patient_objs = Patient.objects.filter(team_id=team_id)
    for patient in patient_objs:
        patient.team_id = None
        patient.bed = None
        patient.ward = None
        patient.save()

    nurs_objs = Account.objects.filter(team_id=team_id, type="Nurse")
    for nurse in nurs_objs:
        nurse.team_id = None
        nurse.save()

    team_inst = Teams.objects.filter(id=team_id)
    team_inst.delete()

    return HttpResponse("Success")
    pass


def reloadteamdata(request):
    id = 1

    all_teams = Teams.objects.all()

    response_data = {}
    team_info = []
    for team in all_teams:
        record = {"id": team.id,
                  "name": team.name,
                  "ward": team.ward}
        team_info.append(record)

    response_data["data"] = team_info
    print("i am in")
    return JsonResponse(json.dumps(response_data), safe=False)
    pass



def returnteaminfo(request):
    print('hi');
    team_id = request.POST.get("teamId")
    nurs_objs = Account.objects.filter(team_id=team_id, type="Nurse")

    response_data = {}
    nurse_info = []
    for nurse in nurs_objs:
        record = {"name": nurse.user.first_name + " " + nurse.user.last_name,
                  "id": nurse.user_id}
        print(record)
        nurse_info.append(record)
    response_data["data"] = nurse_info

    patient_info = []
    patient_objs = Patient.objects.filter(team_id=team_id);
    for patient in patient_objs:
        record = {"name": patient.first_name + " " + patient.last_name,
                  "bed": patient.bed}
        print(record)
        patient_info.append(record)

    response_data["patientdata"] = patient_info
    print(response_data)

    return JsonResponse(json.dumps(response_data), safe=False)




<<<<<<< Updated upstream
=======
    return HttpResponse("success")
    pass


def addteam(request):
    template = loader.get_template('administrator/add_team.html')
    page_name = 'Add Team'    #Fill in here


    context = {
        'page_name': page_name,

    }
    return HttpResponse(template.render(context, request))


def addteamtodb(request):
    print("TEST")
    if request.POST:
        print("TEST2")
        ward_no = request.POST['ward_no']
        team_name = request.POST['team_name']
        print(ward_no)

        team = Teams(name=team_name, ward=ward_no)

<<<<<<< Updated upstream
        team.save()
        return HttpResponse('successful')
>>>>>>> Stashed changes
=======
    return HttpResponse("success")
    pass


def addteam(request):
    template = loader.get_template('administrator/add_team.html')
    page_name = 'Add Team'    #Fill in here


    context = {
        'page_name': page_name,

    }
    return HttpResponse(template.render(context, request))


def addteamtodb(request):
    print("TEST")
    if request.POST:
        print("TEST2")
        ward_no = request.POST['ward_no']
        team_name = request.POST['team_name']
        print(ward_no)

        team = Teams(name=team_name, ward=ward_no)

        team.save()
        return HttpResponse('successful')
>>>>>>> Stashed changes
