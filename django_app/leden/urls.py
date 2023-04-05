from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("signup", views.signup, name="signup"),
    path(
        "login",
        auth_views.LoginView.as_view(
            template_name="registration/login.html", next_page="/"
        ),
        name="login",
    ),
    path("logout", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "password-change",
        auth_views.PasswordChangeView.as_view(
            template_name="registration/password/password_change.html"
        ),
    ),
    path(
        "password-change/done",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="registration/password/password_change_done.html"
        ),
    ),
    path("password-reset", views.password_reset_request, name="password_reset"),
    path(
        "password-reset/done",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("", views.home),
    path("ledenlijst", views.ledenlijst),
    path("profile", views.userinfo, name="user_profile"),
    path("profile/ical", views.ical, name="ical_token"),
    path("profile/edit", views.edit_profile),
    path("new", views.new_leden, name="new_leden"),
    path("<int:lid_id>", views.lid_overview),
]
