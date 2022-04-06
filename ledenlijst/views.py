from django.shortcuts import render
from .models import Lid
from django.contrib.auth import get_user_model

# Create your views here.
from django.shortcuts import render

def ledenlijst(request, *args, **kwargs):
    # User = get_user_model()
    # q = User.objects.all()
    leden = Lid.objects.all()
    context = {
        'leden': leden,
    }
    
    return render(request, 'ledenlijst/ledenlijst.html', context)

