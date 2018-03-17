from django.conf.urls import url
from OKareApp.views import Admin
from OKareApp.views import ManageTeam


urlpatterns = [
    url(r'^$', Admin.index, name="Admin_Index"),
    url(r'^manage_team/', ManageTeam.index, name="ManageTeam_Index"),
    url(r'^manage_patient/', Admin.listPatients, name="ManagePatients"),
    url(r'^view_patient/(?P<patient_id>[\w-]+)$', Admin.viewPatientProfile, name="view_patient"),
    url(r'^manage_task/', Admin.managetask, name="manage_tasks"),
    url(r'^get_patient_tasks/', Admin.getPatientTasks, name="Get_Patient_Tasks"),
    url(r'^get_category_pie_data/', Admin.getCatData, name="Get_Cat_Data"),
    url(r'^get_manage_team_info/', ManageTeam.returnteaminfo, name="ManageTeam_returnteaminfo")
]