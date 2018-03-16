from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.urls import reverse
from django.views import generic
from OKareApp.models import *

def index(request):
    nurse_id = 1
    template = loader.get_template('nurse/template.html')
    #nurse = get_object_or_404(Nurses, pk=nurse_id)
    context = {'nurse': nurse_id}
    return HttpResponse(template.render(context, request))

def listNurses(request):
    template = loader.get_template('nurse/list_nurse.html')
    page_name = 'View Nurse'    #Fill in here

    nurses = Account.objects.filter(type="Nurse")

    context = {
        'page_name': page_name,
        'nurses': nurses,
    }
    return HttpResponse(template.render(context, request))

def viewNurseProfile(request, nurse_id):
    template = loader.get_template('nurse/view_nurse.html')
    page_name = 'View Nurses'    #Fill in here
    nurse_name = 'Nurse Joy'    # From Models

    nurse = Account.objects.filter(user_id=nurse_id).get()

    context = {
        'page_name': page_name,
        'nurse': nurse,
    }
    return HttpResponse(template.render(context, request))

def listPatients(request):
    template = loader.get_template('nurse/list_patient.html')
    page_name = 'View Patients'    #Fill in here

    patients = Patient.objects.all()

    context = {
        'page_name': page_name,
        'patients': patients,
    }
    return HttpResponse(template.render(context, request))

def viewPatientProfile(request, patient_id):
    template = loader.get_template('nurse/view_patient.html')
    page_name = 'View Patient'

    patient = Patient.objects.filter(nric=patient_id).get()

    context = {
                'page_name': page_name,
                'patient_id': patient_id,
                'patient': patient,
               }
    return HttpResponse(template.render(context, request))

def generateProductivityReport(request, nurse_id):
    template = loader.get_template('nurse/productivity_report.html')
    nurse_name = 'Saklani' #From Models
    page_name = 'Generate Productivity Report: ' + nurse_id + " (" + nurse_name + ")"

    context = {
                'page_name': page_name,
                'nurse_id': nurse_id,
                'nurse_name': nurse_name,
               }
    return HttpResponse(template.render(context, request))

def team_tasklist(request):
    team_tasks = Tasks.objects.filter(patient)
    context = {}
    return render(request,'nurse/team_tasklist.html',context)
