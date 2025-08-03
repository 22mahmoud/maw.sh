from django import forms

from src.base.renderers import FormRenderer

from .models import Guestbook
from .utils import render_guestbook_markdown


class GuestbookForm(forms.ModelForm):
    default_renderer = FormRenderer()

    def render_message(self):
        return render_guestbook_markdown(self.cleaned_data["message"])

    class Meta:
        model = Guestbook
        fields = ["name", "emoji", "style", "message", "url", "radius"]
        help_texts = {
            "emoji": "",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "autocomplete": "name",
                    "placeholder": "John Doe",
                    ":value": "form.name",
                    "@input": "updateFormField",
                    "container_class": "col-span-2",
                },
            ),
            "emoji": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    ":value": "form.emoji",
                    "@input": "updateFormField",
                    "container_class": "col-span-1",
                },
            ),
            "message": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Leave a message...",
                    ":value": "form.message",
                    "@input": "updateFormField",
                    "container_class": "col-span-3",
                }
            ),
            "url": forms.URLInput(
                attrs={
                    "autocomplete": "url",
                    "placeholder": "https://your-site.com",
                    ":value": "form.url",
                    "@input": "updateFormField",
                    "container_class": "col-span-3",
                }
            ),
            "style": forms.RadioSelect(
                attrs={
                    ":checked": "isTargetSelected",
                    "@change": "updateFormField",
                    "container_class": "col-span-3",
                    "class": "mt-1 flex flex-row gap-2 flex-wrap",
                }
            ),
            "radius": forms.Select(
                attrs={
                    "@input": "updateFormField",
                    ":selected": "isTargetSelected",
                    "container_class": "max-w-xs",
                }
            ),
        }
