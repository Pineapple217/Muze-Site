from django.urls import path
from . import views

urlpatterns = [
    path('ledenlijst', views.ledenlijst),
    path('signup', views.signup, name='signup'),
]
