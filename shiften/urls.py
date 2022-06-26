from django.urls import path
from . import views

urlpatterns = [
   path('', views.home),
   path('ajax', views.ajax_shift_list),
   path('<int:list_id>', views.shift_list, name='shiftlist'),
   path('<int:list_id>/ajax', views.ajax_shifts),
   path('signup_shift', views.signup_shift, name='signup_shift'),
   path('manage_shift', views.manage_shift),
   path('create_shift', views.create_shift),
]
