from django.urls import path

from .views import contact, validate_contact_field

urlpatterns = [
    path("contact/", contact, name="contact"),
    path("contact/validate/", validate_contact_field, name="validate_contact_field"),
]
