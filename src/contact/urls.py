from django.urls import path

from .views import ContactView, validate_contact_field

urlpatterns = [
    path("", ContactView.as_view(), name="contact"),
    path("validate/", validate_contact_field, name="validate_contact_field"),
]
