from django.urls import path
from . import views

urlpatterns = [
   path('', views.home),
   path('<int:list_id>', views.shift_list, name='shiftlist'),
   path('signup_shift/<int:list_id>', views.signup_shift, name='signup_shift'),
]
