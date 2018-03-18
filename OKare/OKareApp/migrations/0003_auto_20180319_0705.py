# Generated by Django 2.0.3 on 2018-03-18 23:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('OKareApp', '0002_auto_20180319_0639'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read_type', models.CharField(choices=[('Help Requested', 'Help Request Read'), ('Help Accepted', 'Help Accepted')], max_length=100)),
                ('help_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OKareApp.HelpRequest')),
                ('reader', models.ForeignKey(limit_choices_to={'type': 'Nurse'}, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='OKareApp.Account')),
            ],
        ),
        migrations.RemoveField(
            model_name='helprequestnotification',
            name='help_request',
        ),
        migrations.RemoveField(
            model_name='helprequestnotification',
            name='reader',
        ),
        migrations.DeleteModel(
            name='HelpRequestNotification',
        ),
    ]
