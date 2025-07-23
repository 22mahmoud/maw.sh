from django import forms

from .models import Guestbook
from .utils import render_guestbook_markdown


class GuestbookForm(forms.ModelForm):
    class Meta:
        model = Guestbook
        fields = ["name", "emoji", "message", "url", "style", "radius"]

    def render_message(self):
        return render_guestbook_markdown(self.cleaned_data["message"])
