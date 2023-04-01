import calendar
import datetime
import json
from pprint import pprint
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from .forms import AvailableForm, AvailableRepForm, ShiftAddForm, ShiftEditForm, ShiftEditShiftersFrom, ShiftlistCreateForm, ShiftlistCreateWithTemplateForm, ShiftlistEditForm, TemplateForm
from shiften.models import Onbeschikbaar
from leden.models import Lid
from .functions import create_month_shiftlist, get_aviable_shifters
from .models import OnbeschikbaarHerhalend, Shift, Shiftlijst, Template
from django.utils.translation import gettext as _
from django.utils import formats
from django.contrib.auth.models import User
from django.db.models import Q
from itertools import chain


@login_required()
@permission_required('shiften.view_shiftlijst')
def home(request):
    if request.user.has_perm('shiften.change_shiftlijst'):
            shiftlists = Shiftlijst.objects.all()
    else:
            shiftlists = Shiftlijst.objects.filter(is_active=True)
    shiftlists = shiftlists.order_by('date')

    context = {}
    context['form_normal'] = ShiftlistCreateForm()
    context['form_template'] = ShiftlistCreateWithTemplateForm()
    context['shiftlists'] =  shiftlists

    return render(request, 'shiften/home/index.html', context=context)

@login_required()
@permission_required('shiften.add_shiftlijst')
def shiftlist_add_normal(request):
    context = {}
    form = ShiftlistCreateForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            shiftlist = form.save()

            context["list"] = shiftlist
            form = ShiftlistCreateForm()

    context["form_normal"] = form
    return render(request, "shiften/home/add_shiftlist_normal.html", context)

@login_required()
@permission_required('shiften.add_shiftlijst')
def shiftlist_add_template(request):
    context = {}
    form = ShiftlistCreateWithTemplateForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            template_id = form.cleaned_data['template']
            date = form.cleaned_data['date']

            template = Template.objects.get(id=template_id)
            shiftlist = create_month_shiftlist(template, date)
            context["list"] = shiftlist
            form = ShiftlistCreateWithTemplateForm()

    context["form_template"] = form
    return render(request, "shiften/home/add_shiftlist_template.html", context)

@login_required()
@permission_required('shiften.view_shiftlijst')
@permission_required('shiften.view_shift')
def shiftlist(request, shiftlist_id):
    context = {}
    shiftlist = get_object_or_404(Shiftlijst, id  = shiftlist_id)
    context['shiftlist'] = shiftlist
    context['shifts'] = shiftlist.shift_set.all().order_by('date', 'start')
    context['form_edit'] = ShiftlistEditForm(instance=shiftlist)
    context['form_shift'] = ShiftAddForm()
    return render(request, 'shiften/shiftlist/index.html', context=context)

@login_required
@permission_required('shiften.change_shiftlijst')
def shiftlist_edit(request, shiftlist_id):
    context = {}
    shiftlist = get_object_or_404(Shiftlijst, id  = shiftlist_id)
    form = ShiftlistEditForm(request.POST or None, instance=shiftlist)
    if request.method == "POST":
        if form.is_valid():
            shiftlist = form.save()
            context['shiftlist_edited'] = True
            form = ShiftlistEditForm(instance=shiftlist)

    context["shiftlist"] = shiftlist
    context["form_edit"] = form
    return render(request, "shiften/shiftlist/edit_shiftlist.html", context)

@login_required
@permission_required('shiften.delete_shiftlijst')
def shiftlist_delete(request, shiftlist_id):
    shiftlist = get_object_or_404(Shiftlijst, id  = shiftlist_id)
    shiftlist.delete()
    response = HttpResponse()
    response.headers['HX-Redirect'] = reverse('shiftlist_home')
    return response

@login_required()
@permission_required('shiften.view_shift')
def shift_signup(request, shift_id):
    context = {}
    shift = get_object_or_404(Shift, id  = shift_id)
    context['shift'] = shift
    if request.method == "POST":
        user_lid = request.user.lid
        if shift.shifters.contains(user_lid): # zit er all in
            shift.shifters.remove(user_lid)
        elif shift.shifters.count() < shift.max_shifters: # vrije plaats en zit er nog niet in
            shift.shifters.add(user_lid)
        else: # voll
            print("shift voll")

    return render(request, "shiften/shiftlist/shifters_replace_wrapper.html", context)

@login_required()
@permission_required('shiften.view_shift')
def shift_create(request, shiftlist_id):
    context = {}
    shiftlist = get_object_or_404(Shiftlijst, id  = shiftlist_id)
    form = ShiftAddForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            shift = form.save(commit=False)
            shift.shift_list = shiftlist
            shift.save()
            context['new_shift'] = True

            form = ShiftAddForm()
            context['shifts'] = shiftlist.shift_set.all().order_by('date', 'start')

    context['shiftlist'] = shiftlist
    context['form_shift'] = form
    return render(request, "shiften/shiftlist/shift_create.html", context)

@login_required()
@permission_required('shiften.edit_shift')
def shift_edit(request, shift_id):
    context = {}
    shift = get_object_or_404(Shift, id  = shift_id)
    form = ShiftEditForm(request.POST or None, instance=shift)
    if request.method == "POST":
        if form.is_valid():
            shift = form.save()
            context['shifts'] = shift.shift_list.shift_set.all().order_by('date', 'start')
            form = ShiftEditForm(instance=shift)

    context["shift"] = shift
    context["form_edit_shift"] = form
    return render(request, "shiften/shiftlist/shift_edit.html", context)

@login_required
@permission_required('shiften.delete_shift')
def shift_delete(request, shift_id):
    context = {}
    if request.method == "DELETE":
        shift = get_object_or_404(Shift, id  = shift_id)
        shift.delete()
        context['shifts'] = shift.shift_list.shift_set.all().order_by('date', 'start')
        return render(request, "shiften/shiftlist/shift_delete.html", context)

@login_required
@permission_required('shiften.edit_shift')
def shift_edit_shifters(request, shift_id):
    context = {}
    shift = get_object_or_404(Shift, id  = shift_id)
    shiftlist = get_object_or_404(Shiftlijst, id=shift.shift_list.id)
    form = ShiftEditShiftersFrom(request.POST or None, instance = shift)
    context['shift'] = shift
    context['form_edit_shifters'] = form
    print('iets')
    if request.method == 'POST':
        if form.is_valid():
            form.clean()
            form.save()
            return render(request, "shiften/shiftlist/shifters.html", context)
    pprint(get_aviable_shifters(shiftlist))
    return render(request, "shiften/shiftlist/shift_edit_shifters.html", context)

@login_required
@permission_required('shiften.view_shift')
def shift_shifters(request, shift_id):
    context = {}
    shift = get_object_or_404(Shift, id  = shift_id)
    context['shift'] = shift
    return render(request, "shiften/shiftlist/shifters_replace_wrapper.html", context)

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