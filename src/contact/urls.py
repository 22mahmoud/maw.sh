from django.urls import path

from .views import ContactView, validate_contact_field

urlpatterns = [
    path("contact/", ContactView.as_view(), name="contact"),
    path("contact/validate/", validate_contact_field, name="validate_contact_field"),
]
