from django.contrib.auth import authenticate
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from OKareApp.models import Account,Task, CompletedTask, DailyTriage,Patient,NurseStats, OngoingTask, Teams
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist

def login_view(request):
    try:
            if request.method == 'POST':
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    if user.account.type=="Nurse":
                        return render(request, "Nurse.html", {})
                    elif user.account.type=="Admin":
                        return render(request, "Admin.html", {})
                else:
                    messages.error(request, "Invalid")
                return render(request, "login.html", {})
            else:
                return render(request, "login.html", {})
    except ObjectDoesNotExist:
        messages.error(request,"Error")
        return render(request, "login.html", {})