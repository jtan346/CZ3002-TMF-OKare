# Generated by Django 2.0.3 on 2018-03-17 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OKareApp', '0006_auto_20180317_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='date_of_birth',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='patient',
            name='date_of_birth',
            field=models.DateField(),
        ),
    ]