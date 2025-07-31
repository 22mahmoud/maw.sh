from django import forms

from .models import Guestbook
from .utils import render_guestbook_markdown


class GuestbookForm(forms.ModelForm):
    def render_message(self):
        return render_guestbook_markdown(self.cleaned_data["message"])

    class Meta:
        model = Guestbook
        fields = ["name", "emoji", "message", "url", "style", "radius"]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "autocomplete": "name",
                    "placeholder": "John Doe",
                }
            ),
            "emoji": forms.TextInput(attrs={"autocomplete": "off", "help_text": ""}),
            "message": forms.Textarea(attrs={"rows": 5}),
            "style": forms.RadioSelect(),
        }
