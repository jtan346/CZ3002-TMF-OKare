from django.conf.urls import url
from OKareApp.views import Login, Admin, Nurse

urlpatterns = [
    url(r'^$', Login.login_view, name='login')
]
