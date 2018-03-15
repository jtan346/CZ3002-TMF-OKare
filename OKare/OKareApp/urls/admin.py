from django.conf.urls import url
from OKareApp.views import Admin
from OKareApp.views import ManageTeam

urlpatterns = [
    url(r'^$', Admin.index, name="Admin_Index"),
    url(r'^manageteam/', Admin.manageteam, name="ManageTeam_Index"),
    url('path/to/url/', Admin.returnTeamInfo, name ="ManageTeam_returnTeamInfo" )
]