from django.conf.urls import url
from OKareApp.views import Admin

urlpatterns = [
    url(r'^$', Admin.index, name="Admin_Index"),
]