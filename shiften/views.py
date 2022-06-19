from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from MuzeSite.settings import MAX_SHIFTERS_MONTHSHIFT
from django.contrib.auth.decorators import login_required
from shiften.models import Shift, Shiftlijst

# Create your views here.
def home(request):
    shiftlists = Shiftlijst.objects.all()
    context = {
       'shiftlists': shiftlists, 
    }
    return render(request, 'shiften/home.html', context= context)

@login_required()
def shift_list(request, list_id):

    list = get_object_or_404(Shiftlijst, id  = list_id)
    shifts = list.shift_set.all().order_by('date', 'start')
    context = {
        'list': list,
        'shifts': shifts,
        'max_shifters': MAX_SHIFTERS_MONTHSHIFT,
    }
    return render(request, 'shiften/shiftlist.html', context)

login_required()
def signup_shift(request, list_id):
    shift = get_object_or_404(Shift, id = request.POST.get('shift_id'))
    if shift.shifters.contains(request.user.lid):
        shift.shifters.remove(request.user.lid)
    elif(shift.shifters.count() < MAX_SHIFTERS_MONTHSHIFT):
        shift.shifters.add(request.user.lid)
    return HttpResponseRedirect(reverse('shiftlist', args=[str(list_id)])) 