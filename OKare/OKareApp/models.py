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
    date_of_birth = models.DateTimeField(auto_now=True)
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


class NurseStats(models.Model):
    help_requested = models.IntegerField()
    help_administered = models.IntegerField()


class Patient(models.Model):
    nric = models.CharField(max_length=9, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateTimeField(auto_now=True)
    street = models.CharField(max_length=128, default='Street')
    city = models.CharField(max_length=64, default='City')
    state = models.CharField(max_length=32, default='State')
    zip_code = models.CharField(max_length=10, default='Zip Code')
    phoneNo = models.DecimalField(null=True, max_digits=8, decimal_places=0)
    ward = models.CharField(max_length=15)
    bed = models.IntegerField()
    team = models.ForeignKey(Teams, on_delete=None)

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
        return "Task Title: {} | Start Time: {} | Date: {} | Day: {} | patient: {} | recur_type: {}".format(self.title, self.start_time,self.date, self.day, self.patient, self.recur_type)

class OngoingTask(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    nurse = models.OneToOneField(Account, limit_choices_to={'type': 'Nurse'}, on_delete=models.CASCADE)

    def timefrom(self):
        now = datetime.utcnow().replace(tzinfo=timezone.utc)
        difference = (now - datetime.combine(date.today(),self.task.start_time).replace(tzinfo=timezone.utc)).total_seconds()
        #return hours
        if int(difference/3600) >= 1:
            return '{} hours ago...'.format(int(difference / 3600))
        elif int(difference/60) >= 1:
            return '{} minutes ago...'.format(int(difference / 60))
        else:
            return '{} seconds ago...'.format(int (difference))


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
    helper = models.ForeignKey(Account, limit_choices_to={'type':'Nurse'}, related_name='+', on_delete= models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
