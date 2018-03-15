from django.shortcuts import render
from OKareApp.models import Teams
from django.core import serializers
from django.http import HttpResponse
import json
# Create your views here.
def index(Request):

    all_teams = Teams.objects.all()
    context={
        'teams': all_teams
    }

    #return HttpResponse(leads_as_json, content_type='json')
    return render(Request, 'team/manageteam.html', context)
    pass


def returnTeamInfo(Request):
    crisis_id = request.POST.get("name")
    #getAgency = Crisis.objects.get(id = crisis_id)
    response_data = {}
    #if(getAgency.external_agencies is not None or getAgency.external_agencies != ""):
    #    response_data['agency'] = getAgency.external_agencies
    #else:
    #    response_data['agency'] = '';
    reponse_data['name'] = crisis_id;
    return JsonResponse(response_data)
