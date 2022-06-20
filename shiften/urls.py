from django.urls import path
from . import views

urlpatterns = [
   path('', views.home),
   path('<int:list_id>', views.shift_list, name='shiftlist'),
   path('<int:list_id>/ajax', views.ajax_shift_list),
   path('signup_shift/<int:list_id>', views.signup_shift, name='signup_shift'),
]
