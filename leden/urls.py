from django.urls import path
from . import views

urlpatterns = [
    path('ledenlijst', views.ledenlijst),
    path('signup', views.signup, name='signup'),
    path('', views.home),
    path('profile', views.userinfo, name='user_profile'),
    path('profile/edit', views.edit_profile)
]
