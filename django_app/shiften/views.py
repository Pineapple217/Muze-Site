import calendar
import datetime
import json
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseNotFound, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from .forms import AvailableForm, AvailableRepForm
from shiften.models import Onbeschikbaar
from leden.forms import LidSignUpForm
from leden.models import Lid
from .forms import TemplateForm
from .functions import create_month_shiftlist
from .models import OnbeschikbaarHerhalend, Shift, Shiftlijst, Template
from django.utils.translation import gettext as _
from django.utils import formats
from django.contrib.auth.models import User
from django.db.models import Q
from itertools import chain


@login_required()
def home(request):
    if request.user.has_perm("shiften.add_shiftlijst") or request.user.has_perm("shiften.view_template"):
        return render(request, 'shiften/home_perms.html',)
    else:
        shiftlists = Shiftlijst.objects.filter(is_active=True)
        context = {
        'shiftlists': shiftlists, 
        }
        return render(request, 'shiften/home.html', context= context)

@login_required()
def shift_list(request, list_id):
    get_object_or_404(Shiftlijst, id  = list_id)
    return render(request, 'shiften/shiftlist.html')

@login_required()
@permission_required('shiften.view_shift')
def signup_shift(request):
    if request.method == "POST":
        data = json.loads(request.body)
        action = data.get("action")
        id = data.get("shiftId")
        shift = get_object_or_404(Shift, id=id)
        if shift.shift_list.is_active:
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
        else:
            status = 403
            status_msg = "User does not have accesses."

        return JsonResponse({"status": status_msg} ,status = status)

@login_required
def manage_shift(request):
    if request.method == "POST":
        data = json.loads(request.body) 
        action = data.get("action")
        actionInfo = data.get("actionInfo")
        id = actionInfo.get("shiftId")
        shift = Shift.objects.get(id=id)

        dict = {}
        match action:
            case "safe_shifters":
                if request.user.has_perm("shiften.change_shift"):
                    shifters_ids = actionInfo.get("shifters")
                    shift.shifters.clear();
                    for id in shifters_ids:
                        shift.shifters.add(User.objects.get(id=id).lid)
                    dict["status"] = "succes"
                    status = 200
            case "safe_shift":
                if request.user.has_perm("shiften.change_shift"):
                    shift.date = datetime.date.fromisoformat(actionInfo["date"])
                    shift.start = datetime.time.fromisoformat(actionInfo["start"])
                    shift.end = datetime.time.fromisoformat(actionInfo["end"])
                    shift.max_shifters = int(actionInfo["max"])
                    shift.extra_info = actionInfo["info"]
                    shift.save()
                    dict["shift"] = {
                        "string": str(shift).split(" | ")[0]
                    }
                    dict["status"] = "succes"
                    status = 200
            case "delete_shift":
                if request.user.has_perm("shiften.delete_shift"):
                    shift.delete()
                    dict["status"] = "succes"
                    status = 200
            case _:
                status_msg = f"{action}: this action does not exits"
                status = 400 # Bad Request 
        return JsonResponse(dict, status = status)

@login_required() 
@permission_required('shiften.add_shift')
def create_shift(request):
    if request.method == "POST":
        shift_info = json.loads(request.body)
        shift = Shift.objects.create(
                            date = datetime.date.fromisoformat(shift_info["date"]),
                            start =  datetime.time.fromisoformat(shift_info["start"]),
                            end = datetime.time.fromisoformat(shift_info["end"]),
                            max_shifters = shift_info["max"],
                            shift_list = Shiftlijst.objects.get(id = shift_info["shiftList"]),
                            extra_info = shift_info["info"]
                            )
        shift_info = {
            "id": shift.id,
            "date": _(formats.date_format(shift.date, format="l j F")),
            "string": str(shift).split(" | ")[0]
        }
        status_msg = "succes"
        status = 200
        return JsonResponse({"status": status_msg, "shift_info": shift_info }, status = status)

@login_required() 
@permission_required('shiften.view_shift')
def ajax_shifts(request, list_id): 
    list_object = get_object_or_404(Shiftlijst, id  = list_id)
    if list_object.is_active or request.user.has_perm("shiften.change_shift"):
        shifts = list_object.shift_set.all().order_by('date', 'start')
        shifts_dict = []
        for shift in shifts:
            shifters = []
            for u in shift.shifters.all():
                shifters.append({"name": u.user.first_name + " " + u.user.last_name,
                                "id": u.user.id})
            shifts_dict.append({
            "date": shift.date,
            "start":  shift.start.isoformat(timespec = "minutes"),
            "end":  shift.end.isoformat(timespec = "minutes"),
            "shifters": shifters,
            "id": shift.id,
            "max": shift.max_shifters,
            "string": str(shift).split(" | ")[0],
            "info": shift.extra_info,
            })
        list_dict = {
        "date": list_object.date,
        "id" : list_object.id,
        "type": list_object.type, 
        "name": list_object.name,
        "string": str(list_object),
        "is_active": int(list_object.is_active),
        }
        user_dict = {
        "id": request.user.id,
        "name": request.user.first_name + " " + request.user.last_name,
        "perms": {"shift_change"  : request.user.has_perm("shiften.change_shift")if 1 else 0,
                    "shift_add"     : request.user.has_perm("shiften.add_shift")if 1 else 0,
                    "shift_del"     : request.user.has_perm("shiften.delete_shift")if 1 else 0,
                    "shiftlist_edit": request.user.has_perm("shiften.change_shiftlijst")if 1 else 0,
                    "shiftlist_del" : request.user.has_perm("shiften.delete_shiftlijst")if 1 else 0,
                    "available_view": request.user.has_perm("shiften.view_onbeschikbaar")if 1 else 0,}
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
        if request.user.has_perm("shiften.change_shift"):
            dict["types"] = Shiftlijst.type.field.choices
        if request.user.has_perm("shiften.view_onbeschikbaar"):
            dict["available"] = []

            list_first_day = list_object.date.replace(day=1)
            next_month = list_object.date.replace(day=28) + datetime.timedelta(days=4)
            list_last_day = next_month - datetime.timedelta(days=next_month.day)

            avail = Onbeschikbaar.objects.filter(Q(start__lte=list_last_day) & Q(end__gte=list_first_day))
            avail_rep = OnbeschikbaarHerhalend.objects.filter(Q(start_period__lte=list_last_day) & Q(end_period__gte=list_first_day))
            avail_joined = list(chain(avail, avail_rep))
            for a in avail_joined:
                if type(a) == Onbeschikbaar:
                    dict["available"].append({
                        "date": f"{a.start} - {a.end}",
                        "start": a.start,
                        "end": a.end,
                        "info": a.info,
                        "lid": str(a.lid),       
                        "user_id": a.lid.user.id,
                        "type": "normal"
                    })
                if type(a) == OnbeschikbaarHerhalend:
                    subdivided = []
                    # if a.weekday == list_first_day.isoweekday():
                    #     loopday
                    loopday = (a.weekday - list_first_day.isoweekday() + 7)%7
                    if (list_first_day < a.start_period):
                        while (loopday < a.start_period.day):
                            loopday += 7 
                    # if a.start_period.isoweekday() < a.weekday:
                        # start_period_move += datetime.timedelta(a.weekday - a.start_period.isoweekday() - 1)
                    # loopday = start_period_move.day
                    while (loopday < list_last_day.day) and ( (list_first_day + datetime.timedelta(days=loopday)) <= a.end_period):
                        subdivided.append({
                            "date": list_first_day + datetime.timedelta(days=loopday),
                            "start_time": a.start.isoformat(timespec = "minutes"),
                            "end_time": a.end.isoformat(timespec = "minutes"),
                            "info": a.info,
                            "lid": str(a.lid),
                        })
                        loopday += 7
                    dict["available"].append({
                        "date": f"{a.start_period} - {a.end_period}\n{_(calendar.day_name[a.weekday - 1])}\n{a.start} - {a.end}",
                        "info": a.info,
                        "lid": str(a.lid),
                        "user_id": a.lid.user.id,
                        "subs": subdivided,
                        "type": "rep"
                    })
            dict["available"].sort(key=lambda x: x["date"])



                
        status = 200;
    else:
        status = 403
        dict = {"status": "Shiftlist is locked"}
    return JsonResponse(dict, status = status)

@login_required    
@permission_required('shiften.view_shiftlijst')
def ajax_shift_list(request):
    shiftlijsten = []
    if  request.user.has_perm('shiften.change_shiftlijst'):
        shiftlijst_query = Shiftlijst.objects.all()
    else:
        shiftlijst_query = Shiftlijst.objects.filter(is_active=True)
    for shiftlijst in shiftlijst_query:
       shiftlijsten.append({
            "date": shiftlijst.date,
            "type": _(shiftlijst.type),
            "id": shiftlijst.id, 
            "name": shiftlijst.name,
            "string": str(shiftlijst),
            "is_active": shiftlijst.is_active,
       }) 
    user_dict = {
       "id": request.user.id,
       "name": request.user.first_name + " " + request.user.last_name,
       "perms": {"shiftlijst_add": request.user.has_perm("shiften.add_shiftlijst")if 1 else 0,
                 "template_view": request.user.has_perm("shiften.view_template")if 1 else 0,}
    }
    dict = {
        "shiftlists": shiftlijsten,
        "user": user_dict,
    }
    if request.user.has_perm("shiften.add_shiftlijst"):
        dict["types"] = Shiftlijst.type.field.choices
        dict["templates"] = []
        for template in Template.objects.all():
            dict["templates"].append({
                'name': template.name,
                'id': template.id,
            })
    return JsonResponse(dict)   

@login_required
@permission_required('shiften.add_shiftlijst')
def create_shiftlist(request):
    if request.method == "POST":
        data = json.loads(request.body)
        action = data.get("action")
        match action:
            case 'create_shiftlist':
                shiftlist_info = data.get("actionInfo")
                date = datetime.date.fromisoformat(shiftlist_info["date"])
                if shiftlist_info["type"] == "month":
                    date = datetime.date(date.year, date.month, 1)
                shiftlist = Shiftlijst.objects.create(
                                            date = date,
                                            type = shiftlist_info["type"],
                                            name = shiftlist_info["name"],)
                shiftlist_info = {
                "id": shiftlist.id,
                "type": _(shiftlist.type),
                "string": str(shiftlist),
                }

                status_msg = "succes"
                status = 200
            case 'create_shiftlist_template':
                info = data.get("actionInfo")
                template_id = info.get("id")
                shiftlist_date = info.get("vars")
                template = Template.objects.get(id=template_id)
                shiftlist = create_month_shiftlist(template, shiftlist_date)

                shiftlist_info = {
                "date": shiftlist.date,
                "id": shiftlist.id,
                "type": _(shiftlist.type),
                "string": str(shiftlist),
                "name": shiftlist.name
                }
                status_msg = "succes"
                status = 200

            case _:
                status_msg = f"{action}: this action does not exits"
                status = 400 # Bad Request
        return JsonResponse({"status": status_msg, "shiftlist_info": shiftlist_info}, status = status)

@login_required
def manage_shiftlist(request):
    if request.method == "POST":
        data = json.loads(request.body) 
        action = data.get("action")
        actionInfo = data.get("actionInfo")
        id = actionInfo.get("id")
        shiftlijst = Shiftlijst.objects.get(id=id)
        response = {}
        match action:
            case "safe_shiftlist":
                if request.user.has_perm("shiften.change_shiftlijst"):
                    shiftlijst.name = actionInfo.get("name")
                    shiftlijst.date = datetime.date.fromisoformat(actionInfo.get("date"))
                    shiftlijst.type = actionInfo.get("type")
                    shiftlijst.is_active = bool(actionInfo.get("active"))
                    shiftlijst.save()
                    response["shiftlist_info"] = {
                        "type": shiftlijst.type,
                        "string": str(shiftlijst),
                    }
                    status_msg = "succes"
                    status = 200
            case "delete_shiftlist":
                if request.user.has_perm("shiften.delete_shift"):
                    shiftlijst.delete()
                    # mesage dat shift gone is
                    messages.success(request, _("Shiftlist is succesfully deleted"))
                    status_msg = "succes"
                    status = 200
                    # return redirect('shiftlist_home')
            case _:
                status_msg = f"{action}: this action does not exits"
                status = 400 # Bad Request 
        response["status"] = status_msg
        return JsonResponse(response, status = status)

@login_required    
@permission_required('shiften.view_template')
def templates(request):
    templates = Template.objects.all()
    context = {
        'templates': templates,
    }
    return render(request, 'shiften/templates.html', context= context)

@login_required    
@permission_required('shiften.view_template')
def template(request, template_id):
    template = get_object_or_404(Template, id=template_id)
    context = {
       'template': template,
    }

    return render(request, 'shiften/template.html', context= context)

from django.core.mail import EmailMessage
@login_required    
@permission_required('shiften.change_template')
def template_edit(request, template_id):

    template = get_object_or_404(Template, id=template_id)
    if request.method == 'POST':
        template_form = TemplateForm(request.POST, instance=template)
        if template_form.is_valid():
            template_form.save()
            messages.success(request, _('Template updated successfully'))
            url = "/".join(request.path.split("/")[:-1])
            return redirect(url)
    else:
        template_form = TemplateForm(instance = template)
    return render(request, "shiften/template_edit.html", {'form': (template_form)})

@login_required    
@permission_required('shiften.add_template')
def add_template(request):
    if request.method == 'POST':
        template_form = TemplateForm(request.POST)
        if template_form.is_valid():
            template_form.save()
            messages.success(request, _('Template updated successfully'))
            return redirect(to='templates')
    else:
        template_form = TemplateForm()

    return render(request, "shiften/template_create.html", {'form': (template_form)})

@login_required    
@permission_required('shiften.remove_template')
def template_del(request, template_id):
    template = get_object_or_404(Template, id=template_id)
    template.delete()

    return redirect('templates')

@login_required
def available_overview(request):
    today = datetime.date.today()
    av = request.user.lid.onbeschikbaar_set.filter(end__gte = today).order_by('start')
    av_rep = request.user.lid.onbeschikbaarherhalend_set.filter(end_period__gte = today).order_by('start_period')
    context = {
        'available': av,
        'available_rep': av_rep
    }
    # return HttpResponseForbidden()
    return render(request, "shiften/available/overview.html", context)

@login_required
def available_add(request):
    if request.method == 'POST':
        av_form = AvailableForm(request.POST, instance = Onbeschikbaar(lid=request.user.lid))
        if av_form.is_valid():
            av_form.save()
            messages.success(request, _('Available added'))
            return redirect(to='available')
    else:
        av_form = AvailableForm()
    return render(request, "shiften/available/create.html", {'form': (av_form)})

@login_required
def available_add_rep(request):
    if request.method == 'POST':
        av_form = AvailableRepForm(request.POST, instance = OnbeschikbaarHerhalend(lid=request.user.lid))
        if av_form.is_valid():
            av_form.save()
            messages.success(request, _('Available repeating added'))
            return redirect(to='available')
    else:
        av_form = AvailableRepForm()
    return render(request, "shiften/available/create_rep.html", {'form': (av_form)})

@login_required
def available_edit(request, type, available_id):
    match type:
        case 0:
            av = get_object_or_404(Onbeschikbaar, id=available_id)
            if request.method == 'POST':
                av_form = AvailableForm(request.POST, instance=av)
            else:
                av_form = AvailableForm(instance=av)
        case 1:
            av = get_object_or_404(OnbeschikbaarHerhalend, id=available_id)
            if request.method == 'POST':
                av_form = AvailableRepForm(request.POST, instance=av)
            else:
                av_form = AvailableRepForm(instance=av)
        case _:
            return HttpResponseBadRequest()
    
    if not av.lid == request.user.lid:
        return HttpResponseForbidden()
    if request.method == 'POST' and av_form.is_valid():
        av_form.save()
        messages.success(request, _('Availibility updated successfully'))
        return redirect('available')
    # if av.lid == request.user.lid:
        
    # else:
    #     return HttpResponseForbidden()
    return render(request, "shiften/available/edit_rep.html", {'form': (av_form)})

@login_required
def  available_del(request, type, available_id):
    match type:
        case 0:
            av = get_object_or_404(Onbeschikbaar, id=available_id)
        case 1:
            av = get_object_or_404(OnbeschikbaarHerhalend, id=available_id)
        case _:
            return HttpResponseBadRequest()
    
    if av.lid == request.user.lid:
        av.delete()
    else:
        return HttpResponseForbidden()

    return redirect('available')