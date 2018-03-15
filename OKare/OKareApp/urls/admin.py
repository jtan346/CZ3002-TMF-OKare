from django.conf.urls import url
from OKareApp.views import Admin
from OKareApp.views import ManageTeam

urlpatterns = [
    url(r'^$', Admin.index, name="Admin_Index"),
    url('manageteam', ManageTeam.index, name="ManageTeam_Index"),
    url('path/to/url/', ManageTeam.returnTeamInfo, name ="ManageTeam_returnTeamInfo" )
]