from django import forms

from .models import ContactSubmission


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ["name", "email", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "autocomplete": "given-name",
                    "placeholder": "John Doe",
                    "container_class": "w-full md:col-span-1",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "autocomplete": "email",
                    "placeholder": "me@example.com",
                    "container_class": "w-full md:col-span-1",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Your message here...",
                    "container_class": "w-full md:col-span-2",
                }
            ),
        }
