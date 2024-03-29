# Generated by Django 2.0.3 on 2018-03-31 06:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('OKareApp', '0003_notificationbell_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationbell',
            name='help_request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='OKareApp.HelpRequest'),
        ),
        migrations.AlterField(
            model_name='notificationbell',
            name='type',
            field=models.CharField(blank=True, choices=[('Broadcast', 'Broadcast'), ('Response', 'Response'), ('Request', 'Request'), ('Task', 'Task'), ('Assignment', 'Assignment')], max_length=100, null=True),
        ),
    ]
