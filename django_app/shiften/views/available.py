import datetime
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from ..models import OnbeschikbaarHerhalend
from shiften.forms import AvailableForm, AvailableRepForm
from shiften.models import Onbeschikbaar
from django.utils.translation import gettext as _

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