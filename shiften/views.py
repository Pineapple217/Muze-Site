from datetime import date
import json
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from MuzeSite.settings import MAX_SHIFTERS_MONTHSHIFT
from django.contrib.auth.decorators import login_required, permission_required
from leden.models import Lid
from shiften.models import Shift, Shiftlijst
from django.utils.translation import gettext as _
from django.utils import formats
from django.contrib.auth.models import User

@login_required()
def home(request):
    shiftlists = Shiftlijst.objects.all()
    context = {
       'shiftlists': shiftlists, 
    }
    return render(request, 'shiften/home.html', context= context)

@login_required()
def shift_list(request, list_id):
    return render(request, 'shiften/shiftlist.html')

@login_required()
def signup_shift(request):
    if request.method == "POST":
        data = json.loads(request.body)
        action = data.get("action")
        id = data.get("shiftId")
        shift = get_object_or_404(Shift, id=id)
        match action:
            case "add_shifter":
                if shift.shifters.count() < shift.max_shifters:
                    shift.shifters.add(request.user.lid)
                    status_msg = "succes"
                    status = 200 # OK
                else:
                    status_msg = "Shift is full"
                    status = 409 # Conflict 
            case "remove_shifter":
                if shift.shifters.contains(request.user.lid):
                    shift.shifters.remove(request.user.lid)     
                    status_msg = "succes"
                    status = 200 # OK
                else:
                    status_msg = "Shift does not contain given user"
                    status = 409 # Conflict
            case _:
                status_msg = f"{action}: this action does not exits"
                status = 400 # Bad Request

        return JsonResponse({"status": status_msg},status = status)

@login_required
def manage_shift(request):
    if request.method == "POST":
        data = json.loads(request.body) 
        action = data.get("action")
        actionInfo = data.get("actionInfo")
        id = actionInfo.get("shiftId")
        shift = Shift.objects.get(id=id)
        match action:
            case "safe_shifters":
                if request.user.has_perm("shiften.change_shift"):
                    shifters_ids = actionInfo.get("shifters")
                    shift.shifters.clear();
                    for id in shifters_ids:
                        shift.shifters.add(User.objects.get(id=id).lid)
                    status_msg = "succes"
                    status = 200
            case "delete_shift":
                if request.user.has_perm("shiften.delete_shift"):
                    shift.delete()
                    status_msg = "succes"
                    status = 200
            case _:
                status_msg = f"{action}: this action does not exits"
                status = 400 # Bad Request 
        return JsonResponse({"status": status_msg}, status = status)

@login_required() 
@permission_required('shiften.add_shift')
def create_shift(request):
    if request.method == "POST":
        shiftInfo= json.loads(request.body)
        shift = Shift.objects.create(date = date.fromisoformat(shiftInfo["date"]),
                             start =  shiftInfo["start"],
                             end = shiftInfo["end"],
                             max_shifters = shiftInfo["max"],
                             shift_list = Shiftlijst.objects.get(id = shiftInfo["shiftList"]),)
        shift_info ={
            "id": shift.id,
            "date": _(formats.date_format(shift.date, format="l j F")),
        }
        status_msg = "succes"
        status = 200
        return JsonResponse({"status": status_msg, "shift_info": shift_info }, status = status)
    

@login_required() 
@permission_required('shiften.view_shift')
def ajax_shift_list(request, list_id): 
    list = get_object_or_404(Shiftlijst, id  = list_id)
    shifts = list.shift_set.all().order_by('date', 'start')
    shifts_dict = []
    for shift in shifts:
        shifters = []
        for u in shift.shifters.all():
            shifters.append({"name": u.user.first_name + " " + u.user.last_name,
                             "id": u.user.id})
        shifts_dict.append({
        "date": _(formats.date_format(shift.date, format="l j F")),
        "start":  shift.start.isoformat(timespec = "minutes"),
        "end":  shift.end.isoformat(timespec = "minutes"),
        "shifters": shifters,
        "id": shift.id,
        "max": shift.max_shifters,
        # "shift_list": shift.shift_list.id,
        })
    list_dict = {
       "date": _(formats.date_format(list.date , format="F Y")),
       "id" : list.id,
       "type": _(list.type), 
    }
    user_dict = {
       "id": request.user.id,
       "name": request.user.first_name + " " + request.user.last_name,
       "perms": {"shift_change": request.user.has_perm("shiften.change_shift")if 1 else 0,
                 "shift_add"   : request.user.has_perm("shiften.add_shift")if 1 else 0,
                 "shift_del"   : request.user.has_perm("shiften.delete_shift")if 1 else 0,}
    }
    dict = {"shifts": shifts_dict,
            "list": list_dict,
            "user": user_dict,}
    if request.user.has_perm("shiften.change_shift"):
        dict["leden"] = []
        for lid in Lid.objects.all():
            user = lid.user
            dict["leden"].append(
                {"name": user.first_name + " " + user.last_name,
                 "id": user.id,}
            )
    return JsonResponse(dict)