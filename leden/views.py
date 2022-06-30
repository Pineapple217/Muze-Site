from datetime import date
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate

from shiften.models import Shift
from .models import Lid
from .forms import UserSignUpForm, LidSignUpForm
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required , permission_required
from django.contrib.auth.models import Group

def home(request):
    return render(request, 'leden/home.html')

@login_required()
@permission_required('leden.view_lid')
def ledenlijst(request, *args, **kwargs):
    leden = Lid.objects.all()
    context = {
        'leden': leden,
    }
    return render(request, 'leden/ledenlijst.html', context)

def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
                user_form = UserSignUpForm(request.POST)
                lid_form = LidSignUpForm(request.POST)
                if user_form.is_valid() and lid_form.is_valid():
                    user = user_form.save()
                    user.refresh_from_db()
                    lid_form = LidSignUpForm(request.POST, instance = Lid(user=user))
                    lid_form.full_clean()
                    lid_form.save()
                    raw_password = user_form.cleaned_data.get('password1')
                    user = authenticate(username=user.username, password=raw_password)
                    login(request, user)
                    lid_group = Group.objects.get(name='Lid')
                    lid_group.user_set.add(user)
                    messages.success(request, "Welkom bij de muze familie.")
                    return redirect('home')
        else:
            user_form = UserSignUpForm()
            lid_form = LidSignUpForm()
        return render(request, 'leden/signup.html', {'forms': (user_form, lid_form)})
    else:
        return render(request,  'leden/already_logged_in.html')

def userinfo(request):
    shifts = Shift.objects.filter(shifters__id = request.user.lid.id)
    shift_history = shifts.filter(date__range = (start_date, today))
    upcomming_shifts = shifts.filter(date__range = ())
    print(shift_history)
    context = {
        'shift_history': shift_history,
        'upcomming-shifts': upcomming_shifts,
    }
    return render(request, "leden/userinfo.html", context)