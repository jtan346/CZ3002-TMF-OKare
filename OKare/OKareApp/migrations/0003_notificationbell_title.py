# Generated by Django 2.0.2 on 2018-03-28 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OKareApp', '0002_auto_20180328_0222'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationbell',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
