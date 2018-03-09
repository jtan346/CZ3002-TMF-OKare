from django.conf.urls import url
from OKareApp.views import Nurse
urlpatterns = [
    url(r'^$', Nurse.index, name="Nurse_Index"),
]