from django.shortcuts import render
import logging

def home(request):
    logging.error("test")
    return render(request, 'main/home.html')