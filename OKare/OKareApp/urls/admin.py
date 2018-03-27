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
    url(r'^addTask/', Admin.addTask, name="Add_Task"),
    url(r'^editTask/', Admin.editTask, name="Edit_Task"),
    url(r'^getTask/(?P<id>[\w-]+)$', Admin.getTask, name="Get_Task"),
    url(r'^deleteTask/(?P<id>[\w-]+)$', Admin.deleteTask, name="Delete_Task"),
    url(r'^get_category_pie_data/', Admin.getCatData, name="Get_Cat_Data"),
    url(r'^get_manage_team_info/', ManageTeam.returnteaminfo, name="ManageTeam_returnteaminfo"),
    url(r'^get_nurse_with_no_team_info/', ManageTeam.returnnursewithnoteam, name="ManageTeam_nursewithnoteam"),
    url(r'^remove_nurse_from_team/', ManageTeam.removenursefromteam, name="ManageTeam_removenursefromteam"),
    url(r'^remove_patient_from_team/', ManageTeam.removepatientfromteam, name="ManageTeam_removepatientfromteam"),
    url(r'^add_nurse_to_team/', ManageTeam.addnursetoteam, name="ManageTeam_addnursetoteam"),
    url(r'^get_patient_in_team/', ManageTeam.getpatientinteam, name="ManageTeam_getpatientinteam"),
    url(r'^get_patient_with_no_team_info/', ManageTeam.getpatientwithnoteaminfo, name="ManageTeam_getpatientwithnoteaminfo"),
    url(r'^add_patient_to_team/', ManageTeam.addpatienttoteam, name="ManageTeam_addpatienttoteam"),
    url(r'^add_team/', ManageTeam.addteam, name="addteam"),
    url(r'^addteamtodb/', ManageTeam.addteamtodb, name="addteamtodb")
]