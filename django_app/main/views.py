from django.shortcuts import render
import logging

def home(request):
    return render(request, 'main/home.html')