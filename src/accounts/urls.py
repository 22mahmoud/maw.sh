from django.urls import include, path

from .views import profile_view

urlpatterns = [
    path(
        "profile/",
        profile_view,
        name="account_profile",
    ),
    path("", include("allauth.urls")),
]
