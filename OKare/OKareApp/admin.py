from django.contrib import admin
from django.db.models import Model
from OKareApp import models
import inspect

# Register your models here.
try:
    for name,obj in inspect.getmembers(models,inspect.isclass):
        if(issubclass(obj, Model) and name !='User'):
            admin.site.register(obj)
except(TypeError):
    print("Obj Throwing error : %s " % obj)
