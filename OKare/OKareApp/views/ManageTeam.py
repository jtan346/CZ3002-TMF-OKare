from django.shortcuts import render
from OKareApp.models import Teams
from OKareApp.models import Patient
from OKareApp.models import Account
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
import json
from django.template import loader


def is_admin(user):
    return user.account.type == "Admin"

# Create your views here.
@login_required
@user_passes_test(is_admin)
def index(request):
    # Id will get from session once login completed
    id = 1
    activeNurses = Account.objects.filter(type="Nurse").count()
    patientscount = Patient.objects.count()
    teamcount = Teams.objects.count()
    all_teams = Teams.objects.all()
    context = {
        'teams': all_teams,
        'teamcount': teamcount,
        'patientcount':patientscount,
        'activenursecount':activeNurses

    }

    # return HttpResponse(leads_as_json, content_type='json')
    return render(request, 'administrator/manageteam.html', context)
    pass


@login_required
@user_passes_test(is_admin)
def removeteam(request):
    team_id = request.POST.get("teamid")
    print(team_id)
    patient_objs = Patient.objects.filter(team_id=team_id)
    for patient in patient_objs:
        patient.team_id = None
        patient.bed = None
        patient.ward = None
        patient.save()

    nurs_objs = Account.objects.filter(team_id=team_id, type="Nurse")
    for nurse in nurs_objs:
        nurse.team_id = None
        nurse.save()

    team_inst = Teams.objects.filter(id=team_id)
    team_inst.delete()

    return HttpResponse("Success")
    pass

@login_required
@user_passes_test(is_admin)
def reloadteamdata(request):
    id = 1

    all_teams = Teams.objects.all()

    response_data = {}
    team_info = []
    for team in all_teams:
        record = {"id": team.id,
                  "name": team.name,
                  "ward": team.ward}
        team_info.append(record)

    response_data["data"] = team_info
    print("i am in")
    return JsonResponse(json.dumps(response_data), safe=False)
    pass



@login_required
@user_passes_test(is_admin)
def returnteaminfo(request):
    team_id = request.POST.get("teamId")
    nurs_objs = Account.objects.filter(team_id=team_id, type="Nurse")

    response_data = {}
    nurse_info = []
    for nurse in nurs_objs:
        record = {"name": nurse.user.first_name + " " + nurse.user.last_name,
                  "id": nurse.user_id}
        nurse_info.append(record)
    response_data["data"] = nurse_info

    patient_info = []
    patient_objs = Patient.objects.filter(team_id=team_id);
    for patient in patient_objs:
        record = {"name": patient.first_name + " " + patient.last_name,
                  "bed": patient.bed}
        patient_info.append(record)

    response_data["patientdata"] = patient_info

    return JsonResponse(json.dumps(response_data), safe=False)
    pass

@login_required
@user_passes_test(is_admin)
def returnnursewithnoteam(request):
    Tid = request.POST.get("teamId")
    nurs_objs = Account.objects.filter(type="Nurse", team__isnull=True)

    response_data = {}
    nurse_info = []
    for nurse in nurs_objs:
        record = {"name": nurse.user.first_name + " " + nurse.user.last_name,
                  "id": nurse.user_id}
        nurse_info.append(record)
    response_data["data"] = nurse_info;
    return JsonResponse(json.dumps(response_data), safe=False)
    pass

@login_required
@user_passes_test(is_admin)
def removenursefromteam(request):
    jsondata = request.POST.get("data")
    print(jsondata)
    a = "nop"
    if jsondata == a:
        return HttpResponse("success")

    print(jsondata)
    output = jsondata.replace("[", "")
    output = output.replace("]", "")
    output = output.replace("{", "")
    output = output.replace("}", "")
    output = output.replace(":", "")
    output = output.replace("user_id", "")
    output = output.replace("\"", "")
    output = output.split(',')
    print(output)
    number = len(output)
    for x in range(0, number):
        nurseObj = Account.objects.get(user_id=output[x])
        nurseObj.team_id = None
        nurseObj.save()

    print("End of Remove Nurse From Team")
    return HttpResponse("success")
    pass

@login_required
@user_passes_test(is_admin)
def addnursetoteam(request):

    teamid = request.POST.get("teamid")
    jsondata = request.POST.get("data")
    a = "nop"
    if jsondata == a:
        return HttpResponse("success")

    print(jsondata);

    output = jsondata.replace("[", "")
    output = output.replace("]", "")
    output = output.replace("{", "")
    output = output.replace("}", "")
    output = output.replace(":", "")
    output = output.replace("user_id", "")
    output = output.replace("\"", "")
    output = output.split(',')
    print(output)

    number = len(output)
    for x in range(0, number):
        nurseObj = Account.objects.get(user_id=output[x])
        nurseObj.team_id = teamid
        nurseObj.save()

    return HttpResponse("success")
    pass

@login_required
@user_passes_test(is_admin)
def getpatientinteam(request):
    Tid = request.POST.get("teamId")
    patient_obj = Patient.objects.filter(team_id=Tid)

    response_data = {}
    patient_info = []
    for patient in patient_obj:
        record = {"name": patient.first_name + " " + patient.last_name,
                  "nric": patient.nric,
                  "bed": patient.bed}
        patient_info.append(record)
    response_data["data"] = patient_info;
    return JsonResponse(json.dumps(response_data), safe=False)
    pass

@login_required
@user_passes_test(is_admin)
def getpatientwithnoteaminfo(request):
    Tid = request.POST.get("teamId")
    patient_obj = Patient.objects.filter(team__isnull=True)

    response_data = {}
    patient_info = []
    for patient in patient_obj:
        record = {"name": patient.first_name + " " + patient.last_name,
                  "nric": patient.nric}
        patient_info.append(record)
    response_data["data"] = patient_info;
    return JsonResponse(json.dumps(response_data), safe=False)
    pass

@login_required
@user_passes_test(is_admin)
def removepatientfromteam(request):
    jsondata = request.POST.get("data")
    a = "nop"
    if jsondata == a:
        return HttpResponse("success")

    output = jsondata.replace("[", "")
    output = output.replace("]", "")
    output = output.replace("{", "")
    output = output.replace("}", "")
    output = output.replace(":", "")
    output = output.replace("nric", "")
    output = output.replace("\"", "")
    output = output.split(',')
    print(output)
    number = len(output)
    for x in range(0, number):
        patientobj = Patient.objects.get(nric=output[x])
        patientobj.team_id = None
        patientobj.bed = None
        patientobj.ward = None
        patientobj.save()

    print("End of Remove Patient From Team")
    return HttpResponse("success")
    pass

@login_required
@user_passes_test(is_admin)
def addpatienttoteam(request):
    teamid = request.POST.get("teamid")
    wardno = request.POST.get("wardno")
    jsondata = request.POST.get("data")
    a = "nop"
    if jsondata == a:
        return HttpResponse("success")
    output = jsondata.replace("[", "")
    output = output.replace("]", "")
    output = output.replace("{", "")
    output = output.replace("}", "")
    output = output.replace(":", "")
    output = output.replace("nric", "")
    output = output.replace("bed", "")
    output = output.replace("\"", "")
    output = output.split(',')
    print(output)

    number = len(output)
    patientObj = None;
    for x in range(0, number):
        if x%2 == 0:
            patientObj = Patient.objects.get(nric=output[x])
            patientObj.ward = wardno
            patientObj.team_id= teamid
            patientObj.bed = int(output[x+1])
            patientObj.save()

    return HttpResponse("success")
    pass

@login_required
@user_passes_test(is_admin)
def addteam(request):
    template = loader.get_template('administrator/add_team.html')
    page_name = 'Add Team'    #Fill in here


    context = {
        'page_name': page_name,

    }
    return HttpResponse(template.render(context, request))

@login_required
@user_passes_test(is_admin)
def addteamtodb(request):
    print("TEST")
    if request.POST:
        print("TEST2")
        ward_no = request.POST['ward_no']
        team_name = request.POST['team_name']
        print(ward_no)

        team = Teams(name=team_name, ward=ward_no)


        team.save()
        return HttpResponse('successful')

    return HttpResponse("success")
    pass

@login_required
@user_passes_test(is_admin)
def addteam(request):
    template = loader.get_template('administrator/add_team.html')
    page_name = 'Add Team'    #Fill in here


    context = {
        'page_name': page_name,

    }
    return HttpResponse(template.render(context, request))

@login_required
@user_passes_test(is_admin)
def addteamtodb(request):
    print("TEST")
    if request.POST:
        print("TEST2")
        ward_no = request.POST['ward_no']
        team_name = request.POST['team_name']
        print(ward_no)

        team = Teams(name=team_name, ward=ward_no)


        team.save()
        return HttpResponse('successful')

    return HttpResponse("success")
    pass

