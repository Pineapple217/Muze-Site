import datetime
from django.conf import settings
from django.contrib import messages
from django.http import BadHeaderError, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.urls import reverse
from shiften.models import Shift
from .models import Lid
from django.contrib.auth.models import User
from .forms import LidUpdateForm, UserSignUpForm, LidSignUpForm, UserUpdateForm
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required , permission_required
from django.contrib.auth.models import Group
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404
from constance import config
from . import stats

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
                    if Group.objects.filter(name='Lid'):
                        lid_group = Group.objects.get(name='Lid')
                    else:
                        lid_group = Group.objects.create(name='Lid')
                    lid_group.user_set.add(user)
                    send_mail(
                        _("Welkom to The Muze"),
                        render_to_string('leden/mail/succes_signup.html', {'name': user.first_name}),
                        settings.EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=False,
                    )
                    def rvb_email():
                        rvb = User.objects.filter(groups__name='Raad Van Bestuur')                         
                        for rvb_p in rvb:
                            yield rvb_p.email
                        
                    send_mail(
                        _(f"{user.first_name} {user.last_name} wants to become a member"),
                        render_to_string('leden/mail/new_signup.html', {'user': user}),
                        settings.EMAIL_HOST_USER,
                        rvb_email(),
                        fail_silently=False,
                    )
                    messages.success(request, _("Succesfully signed up"))
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
    today = datetime.date.today()
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
    
    return render(request, "leden/edit_profile.html", {'forms': (user_form, lid_form),
                                                       'pp_size': config.PP_MAX_SIZE_MB})

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
                send_mail(
                    _("Welkom to The Muze"),
                    render_to_string('leden/mail/accepted.html', {'name': user.first_name}),
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
            if opt == 'del':
                user.delete()
        return HttpResponseRedirect(reverse("new_leden"))
    new_leden = Lid.objects.filter(is_accepted=False)
    context = {
        "new": new_leden,
    }
    return render(request, "leden/new_leden.html", context)
    
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "registration/password/password_reset_email.html"
                    mail_context = {
                    "email":user.email,
                    'domain': settings.HOST_URL,
                    'site_name': 'Jeughuis De Muze',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, mail_context)
                    try:
                        send_mail(subject, email, settings.EMAIL_HOST_USER , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("password_reset_done")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="registration/password/password_reset.html", context={"form":password_reset_form})

@login_required
@permission_required('leden.view_lid')
def lid_overview(request, lid_id):
    lid = get_object_or_404(Lid, id=lid_id)


    context = {
        "user": lid.user,
        "shifts_in_xmonths": stats.shifts_in_x_months(lid, config.MONTHS_PER_SHIFT),
        "months_per_shift": config.MONTHS_PER_SHIFT,
        "total_shifts": stats.total_shifts_done(lid),
        "days_since_last_shift": stats.days_since_last_shift(lid),
    }
    return render(request, "leden/lid_overview.html", context)