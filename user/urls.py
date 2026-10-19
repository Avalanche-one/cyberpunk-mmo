from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from user.views import (
    ProfileDeleteView,
    ProfileDetailView,
    ProfileUpdateView,
    UserCreateView,
)

app_name = "user"

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(template_name="user/login.html"),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
    path(
        "register/",
        UserCreateView.as_view(),
        name="register",
    ),
    path(
        "profile/",
        ProfileDetailView.as_view(),
        name="profile",
    ),
    path(
        "profile/update/",
        ProfileUpdateView.as_view(),
        name="profile-update",
    ),
    path(
        "profile/delete/",
        ProfileDeleteView.as_view(),
        name="profile-delete",
    ),
]
