from datetime import date
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.urls import reverse
from shiften.models import Shift
from .models import Lid
from django.contrib.auth.models import User
from .forms import LidUpdateForm, UserSignUpForm, LidSignUpForm, UserUpdateForm
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
                    # lid_form.is_accepted = False
                    lid_form.save()
                    raw_password = user_form.cleaned_data.get('password1')
                    user = authenticate(username=user.username, password=raw_password)
                    user.is_active = False
                    user.save()
                    # login(request, user)
                    if Group.objects.filter(name='Lid'):
                        lid_group = Group.objects.get(name='Lid')
                    else:
                        lid_group = Group.objects.create(name='Lid')
                    lid_group.user_set.add(user)
                    send_mail(
                        _("Welkom to The Muze"),
                        render_to_string('leden/mail_succes_signup.html', {'name': user.first_name}),
                        settings.EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=False,
                    )
                    messages.success(request, _("Welkom to the muze"))
                    return redirect('home')
        else:
            user_form = UserSignUpForm()
            lid_form = LidSignUpForm()
        return render(request, 'leden/signup.html', {'forms': (user_form, lid_form)})
    else:
        return render(request,  'leden/already_logged_in.html')

@login_required()
def userinfo(request):
    shifts = Shift.objects.filter(shifters__id = request.user.lid.id).order_by('date')
    today = date.today()
    shift_history = shifts.filter(date__lt = today).reverse()
    upcomming_shifts = shifts.filter(date__gt = today)
    context = {
        'shift_history': shift_history,
        'upcomming_shifts': upcomming_shifts,
    }
    return render(request, "leden/profile.html", context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        lid_form = LidUpdateForm(request.POST, request.FILES, instance=request.user.lid)

        if user_form.is_valid() and lid_form.is_valid():
            user_form.save()
            lid_form.save()
            messages.success(request, _('Your profile is updated successfully'))
            return redirect(to='user_profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        lid_form = LidUpdateForm(instance=request.user.lid)
    return render(request, "leden/edit_profile.html", {'forms': (user_form, lid_form)})

@login_required
@permission_required('leden.accept_lid')
def new_leden(request):
    if request.method == 'POST':
        post_data = request.POST.dict()
        del post_data["csrfmiddlewaretoken"]
        for user_id, opt in post_data.items():
            user = User.objects.get(id=user_id)
            if opt == 'accept':
                user.is_active = True
                user.lid.is_accepted = True
                user.save()
                user.lid.save()
        return HttpResponseRedirect(reverse("new_leden"))
    new_leden = Lid.objects.filter(is_accepted=False)
    context = {
        "new": new_leden,
    }
    return render(request, "leden/new_leden.html", context)