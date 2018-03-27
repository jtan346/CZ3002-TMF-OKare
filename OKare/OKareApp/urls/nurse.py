from django.conf.urls import url
from OKareApp.views import Nurse
from django.views.generic import TemplateView


urlpatterns = [
    #SC/Joey - Nurse Homepage
    url(r'^$', Nurse.index, name="Nurse_Index"),
    # SC/Joey - Nurse Homepage Reloading
    url(r'^current_task$', Nurse.list_current_task, name="current_task"),
    #SC/Joey - Request's Help Request Creation
    url(r'^add_help_request$', Nurse.add_help_request, name="add_help_request"),
    # SC/Joey - Request's Help Request Checking
    url(r'^check_help_request$', Nurse.check_help_request, name="get_help_request"),
    # SC/Joey - Accepter's Help Request Checking
    url(r'^unread_help_request$', Nurse.list_unread_help_request, name="unread_help_request"),

    # SC/Joey - Accepter's Help Request Listing
    url(r'^list_help_request$', Nurse.list_allowed_help_requests, name="list_help_request"),
    # SC/Joey - Accepter's Help Request Reloading
    url(r'^reload_help_request$', Nurse.reload_allowed_help_requests, name="reload_help_request"),

    # SC/Joey - Accepter's Help Request Accepting
    url(r'^accept_help_request$', Nurse.accept_help_request, name="accept_help_request"),

    #SC/Joey - Nurse's Team Tasklist
    url(r'^view_team_tasklist/', Nurse.view_team_tasklist,name="view_team_tasklist"),

    # SC/Joey - Nurse's Complete Task
    url(r'^complete_task/', Nurse.complete_task, name="complete_task"),

    #Ben/HaoDe - List/View Nurse Profiles
    url(r'^view_nurse/$', Nurse.listNurses, name="list_nurse"),
    url(r'^view_nurse/(?P<nurse_id>[\w-]+)$', Nurse.viewNurseProfile, name="view_nurse"),

    #Ben/Haode - List/View Patient Profiles
    url(r'^view_patient/$', Nurse.listPatients, name="list_patient"),
    url(r'^view_patient/(?P<patient_id>[\w-]+)$', Nurse.viewPatientProfile, name="view_patient"),

    #Ben/Haode - Generate Productivity Report
    url(r'productivity_report/(?P<nurse_id>[\w-]+)', Nurse.generateProductivityReport, name="generate_productivity_report"),

    #Ben/Haode - Updating patient or nurse details
    url(r'^update_patient/$', Nurse.updatePatientDetail, name="update_patient_detail"),
    url(r'^update_nurse/$', Nurse.updateNurseDetail, name="update_nurse_detail"),

    #Ben/Haode - View for adding new patient or nurse details
    url(r'^add_nurse/', Nurse.addNurseView, name="add_nurse_view"),
    url(r'^add_patient/', Nurse.addPatientView, name="add_patient_view"),

    #Ben/Haode - Add new patient or nurse
    url(r'^add_patient_into_db/$', Nurse.addPatient, name="add_patient_into_db"),
    url(r'^add_nurse_into_db/$', Nurse.addNurse, name="add_nurse_into_db"),

    #Testing for Noti
    url(r'^updateNotiCount/', Nurse.updateNotiCount),
    url(r'^notificationBell/(?P<slug>[\w-]+)/$', Nurse.nurseNotifications.as_view(), name='notificationBell'), #slug = my account id

]