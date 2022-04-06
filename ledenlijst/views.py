from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .models import Lid
from .forms import UserSignUpForm, LidSignUpForm

# Create your views here.
from django.shortcuts import render

def ledenlijst(request, *args, **kwargs):
    leden = Lid.objects.all()
    context = {
        'leden': leden,
    }
    
    return render(request, 'ledenlijst/ledenlijst.html', context)

def signup(request):
    if request.method == 'POST':
            user_form = UserSignUpForm(request.POST)
            lid_form = LidSignUpForm(request.POST)
            if user_form.is_valid() and lid_form.is_valid():
                user = user_form.save()
                user.refresh_from_db()
                # raw_password = user_form.cleaned_data.get('password1')
                # user = authenticate(username=user.username, password=raw_password)
                # login(request, user)
                lid_form = LidSignUpForm(request.POST, initial=user.lid)
                lid_form.full_clean()
                lid_form.save()
    else:
        user_form = UserSignUpForm()
        lid_form = LidSignUpForm()
    return render(request, 'ledenlijst/signup.html', {'forms': (user_form, lid_form)})
