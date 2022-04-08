from django.urls import path
from . import views

# URLconf
urlpatterns = [
    path('ledenlijst/', views.ledenlijst),
    path('signup/', views.signup)
]
