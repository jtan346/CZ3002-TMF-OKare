from django.conf.urls import url
from OKareApp.views import Nurse

urlpatterns = [
    #SC/Joey - Nurse Homepage
    url(r'^$', Nurse.index, name="Nurse_Index"),

    #SC/Joey - Nurse's Team Tasklist
    url(r'^view_team_tasklist/', Nurse.TeamTaskList.as_view(),name="view_team_tasklist"),

    #Ben/HaoDe - List/View Nurse Profiles
    url(r'^view_nurse/$', Nurse.listNurses, name="list_nurse"),
    url(r'^view_nurse/(?P<nurse_id>[\w-]+)$', Nurse.viewNurseProfile, name="view_nurse"),

    #Ben/Haode - List/View Patient Profiles
    url(r'^view_patient/$', Nurse.listPatients, name="list_patient"),
    url(r'^view_patient/(?P<patient_id>[\w-]+)$', Nurse.viewPatientProfile, name="view_patient"),

    #Ben/Haode - Generate Productivity Report
    url(r'productivity_report/(?P<nurse_id>[\w-]+)', Nurse.generateProductivityReport, name="generate_productivity_report"),

    url(r'^update_patient/$', Nurse.updatePatientDetail, name="update_patient_detail"),
    url(r'^update_nurse/$', Nurse.updateNurseDetail, name="update_nurse_detail"),
]