from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("bestuur", views.bestuur, name="bestuur"),
]
