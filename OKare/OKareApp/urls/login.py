from django.conf.urls import url
from OKareApp.views import Login

urlpatterns = [
    url(r'^$', Login.login_view, name='login')
]
