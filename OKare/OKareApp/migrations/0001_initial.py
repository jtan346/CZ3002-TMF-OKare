from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('nric', models.CharField(max_length=9, primary_key=True, serialize=False)),
                ('date_of_birth', models.DateField()),
                ('street', models.CharField(default='Street', max_length=128)),
                ('city', models.CharField(default='City', max_length=64)),
                ('state', models.CharField(default='State', max_length=32)),
                ('zip_code', models.CharField(default='Zip Code', max_length=10)),
                ('phoneNo', models.DecimalField(decimal_places=0, max_digits=8, null=True)),
                ('type', models.CharField(choices=[('Nurse', 'Nurse'), ('Admin', 'Admin')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CompletedTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.DurationField()),
                ('date', models.DateField()),
                ('compldt', models.DateTimeField(auto_now_add=True)),
                ('nurse', models.ForeignKey(limit_choices_to={'type': 'Nurse'}, on_delete=django.db.models.deletion.CASCADE, to='OKareApp.Account')),
            ],
        ),
        migrations.CreateModel(
            name='DailyTriage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('blood_pressure', models.IntegerField()),
                ('temperature', models.DecimalField(decimal_places=2, max_digits=5)),
                ('blood_sugar', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='HelpRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('acknowledgement', models.BooleanField(default=False)),
                ('helper', models.ForeignKey(limit_choices_to={'type': 'Nurse'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='OKareApp.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read_type', models.CharField(choices=[('Help Requested', 'Help Request Read'), ('Help Accepted', 'Help Accepted')], max_length=100)),
                ('help_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OKareApp.HelpRequest')),
                ('reader', models.ForeignKey(limit_choices_to={'type': 'Nurse'}, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='OKareApp.Account')),
            ],
        ),
        migrations.CreateModel(
            name='NurseStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('help_requested', models.IntegerField()),
                ('help_administered', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='OngoingTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_datetime', models.DateTimeField(auto_now_add=True)),
                ('nurse', models.OneToOneField(limit_choices_to={'type': 'Nurse'}, on_delete=django.db.models.deletion.CASCADE, to='OKareApp.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('nric', models.CharField(max_length=9, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('date_of_birth', models.DateField()),
                ('street', models.CharField(default='Street', max_length=128)),
                ('city', models.CharField(default='City', max_length=64)),
                ('state', models.CharField(default='State', max_length=32)),
                ('zip_code', models.CharField(default='Zip Code', max_length=10)),
                ('phoneNo', models.DecimalField(decimal_places=0, max_digits=8, null=True)),
                ('ward', models.CharField(max_length=15, null=True)),
                ('bed', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, default='')),
                ('recur_type', models.CharField(blank=True, choices=[('Weekly', 'Weekly'), ('Daily', 'Daily'), ('Monthly', 'Monthly')], max_length=100, null=True)),
                ('category', models.CharField(choices=[('Hygiene', 'Hygiene'), ('Medical_Care', 'Medical Care'), ('Therapy', 'Therapy'), ('Food', 'Food'), ('Misc', 'Miscallenous')], default='Misc', max_length=100)),
                ('start_time', models.TimeField()),
                ('date', models.DateField(null=True)),
                ('duration', models.DurationField()),
                ('day', models.CharField(choices=[('0', 'Monday'), ('1', 'Tuesday'), ('2', 'Wednesday'), ('3', 'Thursday'), ('4', 'Friday'), ('5', 'Saturday'), ('6', 'Sunday')], max_length=20)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OKareApp.Patient')),
            ],
        ),
        migrations.CreateModel(
            name='Teams',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('ward', models.CharField(max_length=15)),
            ],
        ),
        migrations.AddField(
            model_name='patient',
            name='team',
            field=models.ForeignKey(null=True, on_delete=None, to='OKareApp.Teams'),
        ),
        migrations.AddField(
            model_name='ongoingtask',
            name='task',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='OKareApp.Task'),
        ),
        migrations.AddField(
            model_name='helprequest',
            name='ongoing_task',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='OKareApp.OngoingTask'),
        ),
        migrations.AddField(
            model_name='helprequest',
            name='requester',
            field=models.ForeignKey(limit_choices_to={'type': 'Nurse'}, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='OKareApp.Account'),
        ),
        migrations.AddField(
            model_name='helprequest',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OKareApp.Task'),
        ),
        migrations.AddField(
            model_name='dailytriage',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OKareApp.Patient'),
        ),
        migrations.AddField(
            model_name='completedtask',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OKareApp.Task'),
        ),
        migrations.AddField(
            model_name='account',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='OKareApp.Teams'),
        ),
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
