from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Avg, Sum
from datetime import datetime, timedelta
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
    ward = models.CharField(max_length=15)
    bed = models.IntegerField()
    team = models.ForeignKey(Teams, on_delete=None)


class Task(models.Model):
    RECURTYPE = (
        ('Weekly','Weekly'),
        ('Daily', 'Daily'),
        ('Monthly', 'Monthly')
    )
    DAY = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )

    CATTYPE = (
        ('Hygiene','Hygiene'),
        ('Medical_Care','Medical Care'),
        ('Therapy','Therapy'),
        ('Food','Food')
    )

    title = models.CharField(max_length=200)
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    recur_type = models.CharField(max_length=100, choices=RECURTYPE, null=True)
    category = models.CharField(max_length = 100, choices=CATTYPE, null=False )
    #all tasks have a start_time, the day of the start time, and date
    start_time = models.TimeField(auto_now=False, editable=True, null=False)
    #only recurring tasks have duration and day
    duration = models.DurationField(editable=True, null=False)
    day = models.CharField(max_length=20, choices=DAY)
    #Date is specifically for tasks that are not recurring
    date = models.DateField(editable=True,null=True, auto_now=False)


class DailyTriage(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateTimeField(editable=True, null=False)
    blood_pressure = models.IntegerField()
    temperature = models.DecimalField(max_digits=5,decimal_places=2)
    blood_sugar = models.IntegerField()


class CompletedTask(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    nurse = models.OneToOneField(Account, limit_choices_to={'type':'Nurse'}, on_delete= models.CASCADE)
    duration = models.DurationField(editable=True, null=False)
    date = models.DateField(editable=True, null=False)

    #make sure to test this Later when DB up (if dont work change back to .aggregate
    def average_duration(self,start_date=datetime.now()-timedelta(days=7)):
        return CompletedTask.Objects.filter(id= self.task.id, date__gte = start_date).Avg('duration')

    def total_tasks_completed(self, nurse_search,start_date=datetime.now()-timedelta(days=7)):
        return CompletedTask.Objects.filter(nurse = nurse_search,date__gte = start_date).Count()

    def total_time_spent(self, nurse_search, start_date=datetime.now()-timedelta(days=7)):
        return CompletedTask.Objects.filter(nurse = nurse_search,date__gte = start_date).Sum('duration')
