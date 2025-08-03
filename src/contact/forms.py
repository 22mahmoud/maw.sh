from django import forms

from src.base.renderers import FormRenderer
from src.contact.models import ContactSubmission


class ContactForm(forms.ModelForm):
    default_renderer = FormRenderer()

    nametest = forms.CharField()

    class Meta:
        model = ContactSubmission
        container_classes = {
            "name": "w-full md:col-span-1",
            "email": "w-full md:col-span-1",
            "message": "w-full md:col-span-2",
        }
        fields = ["name", "email", "message", "nametest"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "autocomplete": "given-name",
                    "placeholder": "John Doe",
                },
            ),
            "email": forms.EmailInput(
                attrs={
                    "autocomplete": "email",
                    "placeholder": "me@example.com",
                },
            ),
            "message": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Your message here...",
                },
            ),
        }
