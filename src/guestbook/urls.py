from django.urls import path

from .views import GuestbookView, validate_guestbook_field

urlpatterns = [
    path("", GuestbookView.as_view(), name="guestbook"),
    path("validate/", validate_guestbook_field, name="validate_guestbook_field"),
]
