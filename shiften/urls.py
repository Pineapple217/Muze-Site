from django.urls import path
from . import views

urlpatterns = [
   path('', views.home, name='shiftlist_home'),
   path('ajax', views.ajax_shift_list),
   path('<int:list_id>', views.shift_list, name='shiftlist'),
   path('<int:list_id>/ajax', views.ajax_shifts),
   path('signup_shift', views.signup_shift, name='signup_shift'),
   path('manage_shift', views.manage_shift),
   path('manage_shiftlist', views.manage_shiftlist),
   path('create_shift', views.create_shift),
   path('create_shiftlist', views.create_shiftlist),
]
