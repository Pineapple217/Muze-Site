from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from shiften.models import Shift, Shiftlijst

# Create your views here.
def home(request):
    return render(request, 'shiften/home.html')

def shift_list(request, list_id):

    list = get_object_or_404(Shiftlijst, id  = list_id)
    shifts = list.shift_set.all().order_by('date', 'start')
    context = {
        'list': list,
        'shifts': shifts,
    }
    return render(request, 'shiften/shiftlist.html', context)

def signup_shift(request, list_id):
    shift = get_object_or_404(Shift, id = request.POST.get('shift_id'))
    if shift.shifters.contains(request.user.lid):
        shift.shifters.remove(request.user.lid)
    else:
        shift.shifters.add(request.user.lid)
    return HttpResponseRedirect(reverse('shiftlist', args=[str(list_id)])) 