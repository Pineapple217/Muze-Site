from dataclasses import dataclass
from email import message
import json
from django.core import serializers
from django.contrib import messages
from django.forms import model_to_dict
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from MuzeSite.settings import MAX_SHIFTERS_MONTHSHIFT
from django.contrib.auth.decorators import login_required
from shiften.models import Shift, Shiftlijst
from django.utils.translation import gettext as _
from django.utils import formats

# Create your views here.
def home(request):
    shiftlists = Shiftlijst.objects.all()
    context = {
       'shiftlists': shiftlists, 
    }
    return render(request, 'shiften/home.html', context= context)

@login_required()
def shift_list(request, list_id):
    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get('message', None)

    list = get_object_or_404(Shiftlijst, id  = list_id)
    shifts = list.shift_set.all().order_by('date', 'start')
    context = {
        'list': list,
        'shifts': shifts,
        'max_shifters': MAX_SHIFTERS_MONTHSHIFT,
    }

    return render(request, 'shiften/shiftlist.html', context)

@login_required()
def signup_shift(request):
    if request.method == "POST":
        data = json.loads(request.body)
        action = data.get("action")
        id = data.get("shiftId", None)
        shift = get_object_or_404(Shift, id=id)
        if action == "add_shifter":
            if shift.shifters.count() < shift.max_shifters:
                shift.shifters.add(request.user.lid)
                status = "done"
            else:
                status = "Shift full"
        if action == "remove_shifter":
            if shift.shifters.contains(request.user.lid):
                shift.shifters.remove(request.user.lid)     
                status = "done"
            else:
                status = "Shift does not contain given user"
        return JsonResponse({"status": status},status = 200)
# @login_required()
# def signup_shift(request, list_id):
#     shift = get_object_or_404(Shift, id = request.POST.get('shift_id'))
#     if shift.shifters.contains(request.user.lid):
#         shift.shifters.remove(request.user.lid)
#     elif(shift.shifters.count() < MAX_SHIFTERS_MONTHSHIFT):
#         shift.shifters.add(request.user.lid)
#     return HttpResponseRedirect(reverse('shiftlist', args=[str(list_id)])) 


@login_required() 
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
    }
    dict = {"shifts": shifts_dict,
            "list": list_dict,
            "user": user_dict}
    return JsonResponse(dict)