from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from OKareApp.models import *
from django.db.models import Q

def login_view(request):
    try:
            if request.method == 'POST':
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request,user)

                    myNotifications = NotificationBell.objects.filter(status=True).filter(
                        Q(type="Broadcast") | Q(type="Request") | Q(target=request.user.account))

                    # upon login, this is the number of UNREAD notifications
                    request.session['unreadNotifications'] = myNotifications.count()
                    request.session['readNotifications'] = 0
                    if user.account.type=="Nurse":
                        return HttpResponseRedirect("/Nurse")
                    elif user.account.type=="Admin":
                        return HttpResponseRedirect("/Admin")
                else:
                    messages.error(request, "Invalid Credentials")
                return render(request, "login.html", {})
            else:
                return render(request, "login.html", {})
    except ObjectDoesNotExist:
        messages.error(request,"User Not Found")
        return render(request, "login.html", {})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/login")

