from django.shortcuts import render
from django.contrib.auth.models import User
import logging


def home(request):
    return render(request, "main/home.html")


def bestuur(request):
    context = {}
    context["rvb"] = User.objects.filter(groups__name="Raad van bestuur")
    context["stuurgroep"] = User.objects.filter(groups__name="Bestuurslid")
    return render(request, "main/bestuur.html", context=context)
