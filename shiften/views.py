from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from MuzeSite.settings import MAX_SHIFTERS_MONTHSHIFT

from shiften.models import Shift, Shiftlijst

# Create your views here.
def home(request):
    shiftlists = Shiftlijst.objects.all()
    context = {
       'shiftlists': shiftlists, 
    }
    return render(request, 'shiften/home.html', context= context)

def shift_list(request, list_id):

    list = get_object_or_404(Shiftlijst, id  = list_id)
    shifts = list.shift_set.all().order_by('date', 'start')
    context = {
        'list': list,
        'shifts': shifts,
        'max_shifters': MAX_SHIFTERS_MONTHSHIFT,
    }
    return render(request, 'shiften/shiftlist.html', context)

def signup_shift(request, list_id):
    shift = get_object_or_404(Shift, id = request.POST.get('shift_id'))
    if shift.shifters.contains(request.user.lid):
        shift.shifters.remove(request.user.lid)
    elif(shift.shifters.count() < MAX_SHIFTERS_MONTHSHIFT):
        shift.shifters.add(request.user.lid)
    # if (shift.shifters.count() == MAX_SHIFTERS_MONTHSHIFT):
        # print('cock')
        # messages.info(request, f'is maximum van {MAX_SHIFTERS_MONTHSHIFT} is al berijkt')
    return HttpResponseRedirect(reverse('shiftlist', args=[str(list_id)])) 