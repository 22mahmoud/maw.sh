from django.urls import include, path

from src.accounts import views

urlpatterns = [
    path(
        "profile/",
        views.profile_view,
        name="account_profile",
    ),
    path("password/reset/", views.password_reset, name="account_reset_password"),
    path("", include("allauth.urls")),
]
