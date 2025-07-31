from django.urls import include, path

from src.accounts import views

urlpatterns = [
    path("profile/", views.ProfileView.as_view(), name="account_profile"),
    path("password/reset/", views.password_reset, name="account_reset_password"),
    path("", include("allauth.urls")),
]
