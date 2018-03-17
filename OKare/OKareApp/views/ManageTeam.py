from django.shortcuts import render
from OKareApp.models import Teams
from OKareApp.models import Patient
from OKareApp.models import Account
from django.http import JsonResponse
from django.core import serializers
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




