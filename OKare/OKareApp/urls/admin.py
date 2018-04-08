from django.conf.urls import url
from OKareApp.views import Admin
from OKareApp.views import ManageTeam


urlpatterns = [
    url(r'^$', Admin.index, name="Admin_Index"),
    url(r'^manage_team/', ManageTeam.index, name="ManageTeam_Index"),
    url(r'^manage_patient/', Admin.listPatients, name="ManagePatients"),
    url(r'^manage_task/', Admin.managetask, name="manage_tasks"),
    url(r'^get_patient_tasks/', Admin.getPatientTasks, name="Get_Patient_Tasks"),
    url(r'^addTask/', Admin.addTask, name="Add_Task"),
    url(r'^editTask/', Admin.editTask, name="Edit_Task"),
    url(r'^getTask/(?P<id>[\w-]+)$', Admin.getTask, name="Get_Task"),
    url(r'^deleteTask/(?P<id>[\w-]+)$', Admin.deleteTask, name="Delete_Task"),
    url(r'^get_nurse_teammates/(?P<id>[\w-]+)$', Admin.getNurseTeammates, name="Get_Nurse_Teammates"),
    url(r'^get_category_pie_data/', Admin.getCatData, name="Get_Cat_Data"),
<<<<<<< HEAD
    url(r'^assign_nurse_hr/', Admin.assignNurseHr, name="Assign_Nurse_HR"),
=======
<<<<<<< Updated upstream
    url(r'^get_manage_team_info/', ManageTeam.returnteaminfo, name="ManageTeam_returnteaminfo")
=======
>>>>>>> T2_Admin
    url(r'^get_manage_team_info/', ManageTeam.returnteaminfo, name="ManageTeam_returnteaminfo"),
    url(r'^get_nurse_with_no_team_info/', ManageTeam.returnnursewithnoteam, name="ManageTeam_nursewithnoteam"),
    url(r'^remove_nurse_from_team/', ManageTeam.removenursefromteam, name="ManageTeam_removenursefromteam"),
    url(r'^remove_patient_from_team/', ManageTeam.removepatientfromteam, name="ManageTeam_removepatientfromteam"),
    url(r'^add_nurse_to_team/', ManageTeam.addnursetoteam, name="ManageTeam_addnursetoteam"),
    url(r'^get_patient_in_team/', ManageTeam.getpatientinteam, name="ManageTeam_getpatientinteam"),
    url(r'^get_patient_with_no_team_info/', ManageTeam.getpatientwithnoteaminfo, name="ManageTeam_getpatientwithnoteaminfo"),
    url(r'^add_patient_to_team/', ManageTeam.addpatienttoteam, name="ManageTeam_addpatienttoteam"),
<<<<<<< HEAD
    url(r'^add_team/', ManageTeam.addteam, name="addteam"),
    url(r'^addteamtodb/', ManageTeam.addteamtodb, name="addteamtodb"),

    #Ben/Haode - List/View Patient Profiles
    url(r'^view_patient/$', Admin.listPatients, name="list_patient"),
    url(r'^view_patient/(?P<patient_id>[\w-]+)$', Admin.viewPatientProfile, name="view_patient"),

    #Ben/HaoDe - List/View Nurse Profiles
    url(r'^view_nurse/$', Admin.listNurses, name="list_nurse"),
    url(r'^view_nurse/(?P<nurse_id>[\w-]+)$', Admin.viewNurseProfile, name="view_nurse"),

    #Ben/Haode - Updating patient or nurse details
    url(r'^update_patient/$', Admin.updatePatientDetail, name="update_patient_detail"),
    url(r'^update_nurse/$', Admin.updateNurseDetail, name="update_nurse_detail"),

    #Ben/Haode - View for adding new patient or nurse details
    url(r'^add_nurse/', Admin.addNurseView, name="add_nurse_view"),
    url(r'^add_patient/', Admin.addPatientView, name="add_patient_view"),

    #Ben/Haode - Add new patient or nurse
    url(r'^add_patient_into_db/$', Admin.addPatient, name="add_patient_into_db"),
    url(r'^add_nurse_into_db/$', Admin.addNurse, name="add_nurse_into_db"),

#Ben/Haode - Generate Productivity Report
    url(r'productivity_report/(?P<nurse_id>[\w-]+)', Admin.generateProductivityReport, name="generate_productivity_report"),
    url(r'^updateNotiCount/', Admin.updateUnreadCount),
    url(r'^notificationBell/(?P<slug>[\w]+)/$', Admin.adminNotifications.as_view(), name='notificationBell'),
    # slug = my account id

=======
    url(r'^reload_team_data/', ManageTeam.reloadteamdata, name="ManageTeam_reloadteamdata"),
    url(r'^remove_team/', ManageTeam.removeteam, name="ManageTeam_removeteam"),
    url(r'^add_team/', ManageTeam.addteam, name="addteam"),
    url(r'^addteamtodb/', ManageTeam.addteamtodb, name="addteamtodb")
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> T2_Admin
]