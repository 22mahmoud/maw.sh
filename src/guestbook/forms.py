from django import forms

from .models import Guestbook


class GuestbookForm(forms.ModelForm):
    class Meta:
        model = Guestbook
        fields = [
            "name",
            "emoji",
            "message",
            "url",
            "bg",
            "text",
            "font",
            "radius",
        ]
