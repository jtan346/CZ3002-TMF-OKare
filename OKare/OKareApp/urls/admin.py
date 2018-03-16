from django.conf.urls import url
from OKareApp.views import Admin

urlpatterns = [
    url(r'^$', Admin.index, name="Admin_Index"),
    url(r'^manageteam/', Admin.manageteam, name="ManageTeam_Index"),
    url(r'^get_category_pie_data/', Admin.getCatData, name="Get_Cat_Data"),
    url('path/to/url/', Admin.returnTeamInfo, name ="ManageTeam_returnTeamInfo" )
]