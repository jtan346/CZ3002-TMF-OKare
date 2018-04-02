from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.urls import reverse
from django.views import generic
from django.db.models import Q
from OKareApp.models import *
import datetime
import datetime
import calendar
import json
from django.core import serializers
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic.list import ListView

def is_nurse(user):
    try:
        return user.account.type == "Nurse"
    except(Exception):
        return False

def assignTask():

    allCompleteTasks = CompletedTask.objects.all()

    #Get all tasks that are not completed/ongoing and need to be started (time < now)

    completeIds = []
    for i in allCompleteTasks:
        # print(i.compldt)
        # print(i.duration)
        endDate = i.compldt
        dur = i.duration
        intendedDate = endDate - dur + timedelta(hours=8)
        print(endDate)
        print(dur)
        print("ID:" + str(i.task_id) + " Start Date:" + str(intendedDate.strftime('%d')))
        if intendedDate.strftime('%d') == datetime.datetime.today().strftime('%d'):
            completeIds.append(i.task.id)

    print("Completed IDs: ")
    print(completeIds)
    toBeAssigned = Task.objects.exclude(id__in=OngoingTask.objects.all().values('task')).exclude(id__in=completeIds).filter(date=date.today()).order_by('start_time')

    #Emulate Task Queue

    taskQueue = []

    for a in toBeAssigned:
        print("to be assigned:")
        print(a.id, a.start_time, datetime.datetime.now().time(), a.start_time < datetime.datetime.now().time())
        if a.start_time < datetime.datetime.now().time():
            taskQueue.append(a)

    #print(len(taskQueue))

    for i in taskQueue:
        #DO THE ASSIGNING GOD
        #GOD SAID LET THERE BE TASKS FOR YOU SLAVE
        #assign i to a nurse

        # Find free nurse(s) in team where patient is from:
        patient = Patient.objects.filter(nric=i.patient_id).get()

        # Requery every round because free nurses must be updated, just assign to first nurse in queryset if any
        print("PATIENT: " + str(patient.team_id))
        freeNurses = Account.objects.exclude(nric__in=OngoingTask.objects.all().values('nurse__nric')).filter(type='Nurse').filter(team_id=patient.team_id)
        #print(patient.team_id)
        #print(freeNurses)
        #Only if got free nurses in team god
        if freeNurses:
            print("Free Nurse ID: " + str(freeNurses[0].nric))
            print("Task ID: " + str(i.id))
            ongoingtask = OngoingTask(assigned_datetime=datetime.datetime.now(), nurse_id=freeNurses[0].nric, task_id=i.id)
            ongoingtask.save()
            notification_bell = NotificationBell(type="Task",target=freeNurses[0], task=i, title="New Task")
            notification_bell.save()


@login_required
@user_passes_test(is_nurse)
def listPatients(request):
    template = loader.get_template('nurse/list_patient.html')
    page_name = 'View Patient'    #Fill in here

    patients = Patient.objects.all()

    context = {
        'page_name': page_name,
        'patients': patients,
    }
    return HttpResponse(template.render(context, request))


@login_required
@user_passes_test(is_nurse)
def viewPatientProfile(request, patient_id):
    template = loader.get_template('nurse/view_patient.html')
    patient = Patient.objects.filter(nric=patient_id).get()
    patient.date_of_birth = patient.date_of_birth.strftime('%d/%m/%Y')
    page_name = str(patient_id) + ": " + patient.first_name + " " + patient.last_name
    teams = Teams.objects.all()

    if patient.team_id:
        try:
            patient_team = Teams.objects.filter(id=patient.team_id).get()
            team_name = str(patient_team.name)
        except AttributeError:
            team_name = ''
    else:
        team_name = ''

    teams = Teams.objects.all()

    context = {
        'page_name': page_name,
        'patient_id': patient_id,
        'patient': patient,
        'teams': teams,
        'team_name': team_name,
        'accountid': request.user.account.nric,
    }

    return HttpResponse(template.render(context, request))


@login_required
@user_passes_test(is_nurse)
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
            team = request.POST['team']

            patient = Patient.objects.get(nric=nric)

            #Format date..
            converted_datetime = datetime.strptime(date_of_birth, "%d/%m/%Y")

            # patient.nric = nric
            patient.first_name = first_name
            patient.last_name = last_name
            patient.date_of_birth = converted_datetime
            patient.ward = ward
            patient.bed = bed
            patient.street = street
            patient.city = city
            patient.state = state
            patient.zip_code = zip_code
            patient.phoneNo = phone_no

            if team != 'No Allocation':
                patient.team = Teams.objects.filter(name=team).get()
            else:
                patient.team_id = None

            patient.save()

        except(KeyError, Patient.DoesNotExist):
            return HttpResponse('unsuccessful')

        else:
            return HttpResponse('successful')


@login_required
@user_passes_test(is_nurse)
def view_team_tasklist(request):
    #team is from nurse's team, retrieved from user, awaiting completion of login
    #team_tasks = Task.objects.filter(start_time__gte=datetime.datetime.now(), patient__team=request.user.account.team).exclude(~Q(date__day=datetime.datetime.now().day), Q(recur_type='Monthly') | Q(recur_type__isnull=True))
    #team_tasks = Task.objects.filter(patient__team=request.user.account.team)

    allCompleteTasks = CompletedTask.objects.all()

    # Get all tasks that are not completed/ongoing and need to be started (time < now)

    completeIds = []
    for i in allCompleteTasks:
        # print(i.compldt)
        # print(i.duration)
        endDate = i.compldt
        dur = i.duration
        intendedDate = endDate - dur + timedelta(hours=8)
        print(endDate)
        print(dur)
        print("ID:" + str(i.task_id) + " Start Date:" + str(intendedDate.strftime('%d')))
        if intendedDate.strftime('%d') == datetime.datetime.today().strftime('%d'):
            completeIds.append(i.task.id)

    print("Completed IDs: ")
    print(completeIds)
    team_tasks = Task.objects.exclude(id__in=OngoingTask.objects.all().values('task')).exclude(
        id__in=completeIds).filter(date=date.today()).order_by('start_time')


    context = { "team_tasks": team_tasks,
                'name': request.user.first_name,
                'usertype': request.user.account.type,
                'accountid': request.user.account.nric
                }
    return render(request,'nurse/team_tasklist.html',context)

@login_required
@user_passes_test(is_nurse)
def index(request):
    assigned_task = OngoingTask.objects.filter(nurse=request.user.account).first()
    assignTask()


    context = { 'assigned_task':assigned_task,
                'name': request.user.first_name,
                'usertype': request.user.account.type,
                'accountid': request.user.account.nric
                }

    return render(request,'nurse/index.html', context)

@login_required
@user_passes_test(is_nurse)
def list_current_task(request):
    assigned_task = OngoingTask.objects.filter(nurse=request.user.account).first()
    context = { 'assigned_task':assigned_task }
    return render(request,'nurse/ui_components/current_task.html', context)

@login_required
@user_passes_test(is_nurse)
def complete_task(request):
    if request.method =="POST":
        try:
            assigned_task = OngoingTask.objects.filter(nurse=request.user.account).first()
            duration = datetime.datetime.now() - assigned_task.assigned_datetime
            print(duration)
            completed_task = CompletedTask(task=assigned_task.task, date=assigned_task.task.date,
                                           nurse=assigned_task.nurse, duration=duration)
            completed_task.save()
            assigned_task.delete()
            #assignTask()
        except(Exception):
            print(Exception)
            return HttpResponse("FAILURE")
        else:
            return HttpResponse("SUCCESS")

@login_required
@user_passes_test(is_nurse)
def add_help_request(request):
    if request.method == "POST":
        try:
            account = request.user.account
            current_task = OngoingTask.objects.get(nurse=account)
            help_request = HelpRequest(requester=account, helper=None, task=current_task.task, ongoing_task=current_task, time_created=datetime.datetime.now())
            help_request.save()
            notification_bell = NotificationBell(type="Request", task=current_task.task, title="Help needed", help_request=help_request)
            notification_bell.save()
        except(KeyError, Account.DoesNotExist):
            return HttpResponse("Failure")
        else:
            return HttpResponse("Success")

#list help requests lists all the help requests for a person to accept
@login_required
@user_passes_test(is_nurse)
def list_unread_help_request(request):
    #assignTask()
    account = request.user.account
    help_requests = HelpRequest.objects.filter(Q(requester__team=account.team) & ~Q(requester=account), helper__isnull=True).exclude(
        id__in=Notification.objects.filter(reader=account, read_type="Help Requested").values('help_request'))

    print(help_requests)
    for help_request in help_requests:
        i_read_this = Notification(reader=account, help_request=help_request, read_type="Help Requested")
        i_read_this.save()

    context = { 'help_requests' : help_requests }
    # this gives you a list of dicts
    raw_data = serializers.serialize('python', help_requests)
    # now extract the inner `fields` dicts
    actual_data = [d['fields'] for d in raw_data]

    for request in actual_data:
        nric = request['requester']
        request['requester'] = Account.objects.get(nric=nric).fullname()
        del request['time_created']

    # and now dump to JSON
    return JsonResponse(actual_data,safe=False)

@login_required
@user_passes_test(is_nurse)
def list_allowed_help_requests(request):
    account = request.user.account
    #filter all help request which are no in the same team as the requester, and not those generated by the requester so that the poller
    #only sees help requests in his own team, and those that do not belong to him
    #exclude past help requests where the user helped
    #allowed_help_requests = HelpRequest.objects.filter(Q(requester__team=account.team) & ~Q(requester=account), helper__isnull=True). \
    #    exclude(ongoing_task__in=HelpRequest.objects.filter(helper=account).values('ongoing_task'))

    allowed_help_requests = HelpRequest.objects.filter(Q(requester__team=account.team) & ~Q(requester=account), helper__isnull=True)

    try:
        ongoing_task = OngoingTask.objects.get(nurse=account)
        created_help_requests = HelpRequest.objects.filter(requester=account, ongoing_task=ongoing_task)
    except (OngoingTask.DoesNotExist):
        created_help_requests = None

    context = {
        'created_help_requests' : created_help_requests,
        'allowed_help_requests' : allowed_help_requests,
        'name': request.user.first_name,
        'usertype': request.user.account.type,
        'accountid': request.user.account.nric
    }

    return render(request, 'nurse/help_requests.html', context)

@login_required
@user_passes_test(is_nurse)
def reload_allowed_help_requests(request):
    account = request.user.account
    #filter all help request which are no in the same team as the requester, and not those generated by the requester so that the poller
    #only sees help requests in his own team, and those that do not belong to him
    #exclude help requests for tasks which he has responded to
    # allowed_help_requests = HelpRequest.objects.filter(Q(requester__team=account.team) & ~Q(requester=account), helper__isnull=True). \
    #     exclude(ongoing_task__in=HelpRequest.objects.filter(helper=account).values('ongoing_task'))
    allowed_help_requests = HelpRequest.objects.filter(Q(requester__team=account.team) & ~Q(requester=account),helper__isnull=True)
    print("HELLO")
    print(allowed_help_requests)
 #    try:
    ongoing_task = OngoingTask.objects.get(nurse=account)
    created_help_requests = HelpRequest.objects.filter(requester=account, ongoing_task=ongoing_task)
 #   except (OngoingTask.DoesNotExist):
#        created_help_requests = None

    context = {
        'created_help_requests' : created_help_requests,
        'allowed_help_requests' : allowed_help_requests,
        'name': request.user.first_name,
        'usertype': request.user.account.type,
        'accountid': request.user.account.nric
    }

    return render(request, 'nurse/ui_components/help_requests.html', context)

#check help request returns a list of help requests initiated by the account to see if they are acepted
@login_required
@user_passes_test(is_nurse)
def check_help_request(request):
    account = request.user.account
    try:
        ongoing_task = OngoingTask.objects.get(nurse=account)
        help_requests = HelpRequest.objects.filter(requester=account, acknowledgement=False, helper__isnull=False, ongoing_task=ongoing_task).\
            exclude(id__in=Notification.objects.filter(reader=account, read_type="Help Accepted").values('help_request'))

        for help_request in help_requests:
            i_read_this = Notification(reader=account, help_request=help_request, read_type="Help Accepted")
            i_read_this.save()

        # .update(acknowledgement=True)
        # this gives you a list of dicts
        raw_data = serializers.serialize('python', help_requests)
        # now extract the inner `fields` dicts
        actual_data = [d['fields'] for d in raw_data]

        for request in actual_data:
            nric = request['helper']
            request['helper'] = Account.objects.get(nric=nric).fullname()
            del request['time_created']
    except(Exception):
        actual_data = {}

    # and now dump to JSON
    return JsonResponse(actual_data,safe=False)

@login_required
@user_passes_test(is_nurse)
def check_assigned_help_request(request):
    account = request.user.account
    try:
        help_requests = HelpRequest.objects.filter(id__in=NotificationBell.objects.filter(type="Assignment", target=account, help_request__ongoing_task__in=OngoingTask.objects.all()).values('help_request')).\
            exclude(id__in=Notification.objects.filter(reader=account, read_type="Help Accepted").values('help_request'))

        for help_request in help_requests:
            i_read_this = Notification(reader=account, help_request=help_request, read_type="Help Accepted")
            i_read_this.save()

            # .update(acknowledgement=True)
            # this gives you a list of dicts
        raw_data = serializers.serialize('python', help_requests)
            # now extract the inner `fields` dicts
        actual_data = [d['fields'] for d in raw_data]

        for help_request in actual_data:
            nric = help_request['requester']
            help_request['requester'] = Account.objects.get(nric=nric).fullname()
            del help_request['time_created']

    except(Exception):
        actual_data = {}

    return JsonResponse(actual_data,safe=False)

@login_required
@user_passes_test(is_nurse)
def accept_help_request(request):
    account = request.user.account
    help_request_id = request.POST.get("id")
    help_request = HelpRequest.objects.filter(id=help_request_id).get()
    help_request.helper = account
    help_request.save()
    NotificationBell.objects.filter(type="Request", task=help_request.task).update(status=False)
    notification_bell = NotificationBell(type="Response", target=help_request.requester, title="Your request was accepted")
    notification_bell.save()
    return HttpResponse("OKAY")

class nurseNotifications(LoginRequiredMixin,UserPassesTestMixin, ListView):
    template_name = 'nurse/ui_components/notificationBell.html'

    def test_func(self):
        try:
            dataRec = self.kwargs['slug']
            data2 = dataRec.replace('-', ' ').split(' ')
            account = Account.objects.filter(nric=data2[0]).get()
            return account.type == "Nurse"
        except(Exception):
            return False

    def get_queryset(self):
        myNotifications = NotificationBell.objects.filter(status=True).filter(Q(type="Broadcast") | Q(type="Request")  | Q(target=self.request.user.account))
        return myNotifications

    def get_context_data(self, **kwargs):

        dataRec = self.kwargs['slug']
        data2 = dataRec.replace('-', ' ').split(' ')
        curAccount = Account.objects.filter(nric=data2[0]).get()
        myNotifications = NotificationBell.objects\
            .filter(status=True).filter(Q(type="Broadcast") | ( Q(type="Request") & ~Q(help_request__requester=curAccount) & Q(help_request__requester__team=curAccount.team))| Q(target=curAccount) |
                                        (Q(type="Assignment") & Q(help_request__helper=curAccount) & Q(help_request__ongoing_task__in=OngoingTask.objects.all()))
                                        )

        self.request.session['currentNotifications'] = myNotifications.count()

        if self.request.session['currentNotifications'] > self.request.session['readNotifications']:
            self.request.session['unreadNotifications'] = self.request.session['currentNotifications'] - self.request.session['readNotifications']

        print("curNotis:" + str(self.request.session['currentNotifications']))
        print("curUnread:" + str(self.request.session['unreadNotifications']))
        print("curRead:" + str(self.request.session['readNotifications']))

        context = {
            'myNotifications': myNotifications,  #All notifications
            'unreadNotifications': self.request.session['unreadNotifications'],
            'curTime': datetime.datetime.now(),
            'accountid': self.request.user.account.nric
        }

        return context

def updateUnreadCount(request):
    print("updateNotiCount")
    request.session['readNotifications'] += request.session['unreadNotifications']
    request.session['unreadNotifications'] = 0
    return HttpResponse('')

#upon system start (currently should have no notifications at startup) populate Notification Model
def initNotifications(request):

    #At startup, there should only be new (Ongoing) Tasks after assignation by algorithm, no help requests or broadcasts.

    allOngoingTasks = OngoingTask.objects.all()

    for n in allOngoingTasks:
        newNoti = NotificationBell(type="Task", target=n.nurse, task=n.task, title="New Task")
        newNoti.save()

    return HttpResponse('')


def getCurrentNotiCount(userid):
    print(userid)
    curAccount = Account.objects.filter(nric=userid).get()
    myNotifications = NotificationBell.objects.filter(status=True).filter(Q(type="Broadcast") | Q(type="Request") | Q(target=curAccount))
    return myNotifications.count()

#Unread Notifications moved to login Manager

