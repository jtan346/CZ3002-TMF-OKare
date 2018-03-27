from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Avg, Sum
from datetime import datetime, timedelta, timezone, date
# Create your models here.

class Teams(models.Model):
    name = models.CharField(max_length=30)
    ward = models.CharField(max_length=15)

class Account(models.Model):
    nric = models.CharField(max_length=9, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    TYPES = (
        ('Nurse', 'Nurse'),
        ('Admin', 'Admin')
    )
    date_of_birth = models.DateField(auto_now=False, editable=True)
    street = models.CharField(max_length=128, default='Street')
    city = models.CharField(max_length=64, default='City')
    state = models.CharField(max_length=32, default='State')
    zip_code = models.CharField(max_length=10, default='Zip Code')
    phoneNo = models.DecimalField(null=True,max_digits=8,decimal_places=0)
    type = models.CharField(max_length=100, choices=TYPES)
    team = models.ForeignKey(Teams, on_delete=models.SET_NULL, null=True)

    def clean(self, *args, **kwargs):
        if self.type == "Admin" and self.team != None:
            raise ValueError("Admin should not have team")

        super(Account, self).clean(*args, **kwargs)

    def __str__(self):
        return "NRIC: {} | TYPE: {} | TEAM: {} | Username: {}".format(self.nric, self.type, self.team, self.user.username)

    def fullname(self):
        return self.user.first_name + " " + self.user.last_name

class NurseStats(models.Model):
    help_requested = models.IntegerField()
    help_administered = models.IntegerField()


class Patient(models.Model):
    nric = models.CharField(max_length=9, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(auto_now=False, editable=True, blank=False, null=False)
    street = models.CharField(max_length=128, default='Street')
    city = models.CharField(max_length=64, default='City')
    state = models.CharField(max_length=32, default='State')
    zip_code = models.CharField(max_length=10, default='Zip Code')
    phoneNo = models.DecimalField(null=True, max_digits=8, decimal_places=0)
    ward = models.CharField(null=True, max_length=15)
    bed = models.IntegerField(null=True)
    team = models.ForeignKey(Teams, on_delete=None, null=True)

    def name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.first_name + " " + self.last_name

class Task(models.Model):
    RECURTYPE = (
        ('Weekly','Weekly'),
        ('Daily', 'Daily'),
        ('Monthly', 'Monthly')
    )
    DAY = (
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday'),
    )

    CATTYPE = (
        ('Hygiene','Hygiene'),
        ('Medical_Care','Medical Care'),
        ('Therapy','Therapy'),
        ('Food','Food'),
        ('Misc','Miscallenous')
    )

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True, default="")

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    recur_type = models.CharField(max_length=100, choices=RECURTYPE, null=True, blank=True)

    category = models.CharField(max_length = 100, choices=CATTYPE, null=False, default='Misc')

    #all tasks have a date, and the start time
    start_time = models.TimeField(auto_now=False, editable=True, null=False)
    date = models.DateField(editable=True,null=True, auto_now=False)

    #duration is stored, because it's easier than calculating the start_time between 2 tasks
    duration = models.DurationField(editable=True, null=False)

    #day is only for weekly tasks, simplifies retrieving the day otherwise we need to have complex
    #day retrieval from the date
    day = models.CharField(max_length=20, choices=DAY)

    def __str__(self):
        return "ID : {} | Task Title: {} | Start Time: {} | Date: {} | Day: {} | patient: {} | recur_type: {}".format(self.id, self.title, self.start_time,self.date, self.day, self.patient, self.recur_type)

class OngoingTask(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    nurse = models.OneToOneField(Account, limit_choices_to={'type': 'Nurse'}, on_delete=models.CASCADE)
    #to track when it was assigned, for computation of duration
    #  if a daily task was assigned on monday at 11:50, and was finished tuesday at 00:25
    #  then the task's date captures the date of creation
    assigned_datetime = models.DateTimeField(auto_now_add=True)
    def timefrom(self):
        now = datetime.now().replace(tzinfo=timezone.utc)
        difference = (now - datetime.combine(date.today(),self.task.start_time).replace(tzinfo=timezone.utc)).total_seconds()
        #return hours
        if int(difference/3600) >= 1:
            return '{} hours ago...'.format(int(difference / 3600))
        elif int(difference/60) >= 1:
            return '{} minutes ago...'.format(int(difference / 60))
        else:
            return '{} seconds ago...'.format(int (difference))

    def __str__(self):
        return "Ongoing Task - {} : {} assigned to {} ".format(self.id, self.task.title, self.nurse.nric)


class DailyTriage(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateTimeField(editable=True, null=False)
    blood_pressure = models.IntegerField()
    temperature = models.DecimalField(max_digits=5,decimal_places=2)
    blood_sugar = models.IntegerField()


class CompletedTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    nurse = models.ForeignKey(Account, limit_choices_to={'type':'Nurse'}, on_delete= models.CASCADE)
    duration = models.DurationField(editable=True, null=False)
    date = models.DateField(editable=True, null=False)
    compldt = models.DateTimeField(auto_now_add=True, editable=True)
    #make sure to test this Later when DB up (if dont work change back to .aggregate
    def average_duration(self,start_date=datetime.now()-timedelta(days=7)):
        return CompletedTask.objects.filter(id= self.task.id, date__gte = start_date).Avg('duration')

    def total_tasks_completed(self,start_date=datetime.now()-timedelta(days=7)):
        return CompletedTask.objects.filter(date__gte = start_date).Count()

    def total_tasks_completed_nurse(self, nurse_search,start_date=datetime.now()-timedelta(days=7)):
        return CompletedTask.objects.filter(nurse = nurse_search,date__gte = start_date).Count()

    def total_time_spent(self, nurse_search, start_date=datetime.now()-timedelta(days=7)):
        return CompletedTask.objects.filter(nurse = nurse_search,date__gte = start_date).Sum('duration')


class HelpRequest(models.Model):
    # '+' prevents the Account from being able to access request and helper
    requester = models.ForeignKey(Account, limit_choices_to={'type':'Nurse'},related_name='+', on_delete= models.CASCADE)
    helper = models.ForeignKey(Account, limit_choices_to={'type':'Nurse'}, related_name='+', on_delete= models.CASCADE, null=True)
    #when an ongoing task is deleted, there is no more reference to a task; there is no way to find out the help request was for which task
    #at this point it can be tied to a completed task but it is simplified to only task. Change to completed task if required
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    time_created =models.DateTimeField(editable=True, null=False)
    ongoing_task = models.ForeignKey(OngoingTask, on_delete=models.SET_NULL, null=True)
    acknowledgement = models.BooleanField(default=False)

    def status(self):
        if(self.helper == None):
            return None
        else:
            return self.helper.fullname()

    def __str__(self):
        return "Task: {} | Requester: {} | Helper: {} | Ongoing Tasks: {}".format(self.task.title, self.requester, self.helper, self.ongoing_task)

    def timecreated(self):
        now = datetime.now().replace(tzinfo=timezone.utc)
        difference = (now - self.time_created).seconds
        # return hours
        if int(difference / 3600) >= 1:
            return '{} hours ago...'.format(int(difference / 3600))
        elif int(difference / 60) >= 1:
            return '{} minutes ago...'.format(int(difference / 60))
        else:
            return '{} seconds ago...'.format(int(difference))

    def requestor_name(self):
        return self.requester.fullname()


class Notification(models.Model):
    type = (
        ("Help Requested", "Help Request Read"),
        ("Help Accepted",  "Help Accepted")
    )
    read_type = models.CharField(choices=type, max_length=100)
    reader = models.ForeignKey(Account, limit_choices_to={'type':'Nurse'},related_name='+', on_delete= models.CASCADE)
    help_request = models.ForeignKey(HelpRequest, on_delete=models.CASCADE)

    def __str__(self):
        return "reader: {} for help request {}".format(self.reader.fullname(), self.help_request.id)

class NotificationBell(models.Model):
    types = (
        ("Broadcast", "Broadcast"), #To All Nurses/Admins
        ("Response", "Response"),   #When my Help Request is responded to (Single Nurse Target)
        ("Request", "Request"),     #When there is new Help Request (Broadcast to all Nurses)
        ("Task", "Task")            #When there is a new Task assigned (From ongoingtask, single target)
    )
    target = models.ForeignKey(Account, null=True, blank=True, on_delete=models.CASCADE) #Notification for Target (Single) Nurse, when type = Response, else null
    task = models.ForeignKey(Task, null=True, blank=True, on_delete=models.CASCADE) #Only for ongoing task and help request, can be null
    type = models.CharField(choices=types, max_length=100, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    status = models.BooleanField(default=True) #Set to false if notification is over by event (i.e. when help request is fulfilled or task is completed
