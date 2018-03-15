from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.urls import reverse
from django.views import generic

from OKareApp.models import Account,Task, CompletedTask, DailyTriage,Patient,NurseStats

def index(request):
    nurse_id = 1
    #nurse = get_object_or_404(Nurses, pk=nurse_id)
    context = {'nurse': nurse_id}

def listNurses(request):
    template = loader.get_template('nurse/list_nurse.html')
    page_name = 'View Nurse'    #Fill in here

    context = {
        'page_name': page_name,
    }
    return HttpResponse(template.render(context, request))

def viewNurseProfile(request, nurse_id):
    template = loader.get_template('nurse/view_nurse.html')
    page_name = 'View Nurses'    #Fill in here
    nurse_name = 'Nurse Joy'    # From Models

    context = {
        'page_name': page_name,
        'nurse_id': nurse_id,
        'nurse_name': nurse_name,
    }
    return HttpResponse(template.render(context, request))

def listPatients(request):
    template = loader.get_template('nurse/list_patient.html')
    page_name = 'View Patients'    #Fill in here

    context = {
        'page_name': page_name,
    }
    return HttpResponse(template.render(context, request))

def viewPatientProfile(request, patient_id):
    template = loader.get_template('nurse/view_patient.html')
    page_name = 'View Patient'
    patient_name = 'Benjamin' #From Models
    context = {
                'page_name': page_name,
                'patient_id': patient_id,
                'patient_name': patient_name,
               }
    return HttpResponse(template.render(context, request))

def team_tasklist(request):
    team_tasks = Tasks.objects.filter(patient)
    context = {}
    return render(request,'nurse/team_tasklist.html',context)
