from django import forms
from django_recaptcha import fields, widgets

from .models import ContactSubmission


class ContactForm(forms.ModelForm):
    captcha = fields.ReCaptchaField(widget=widgets.ReCaptchaV3(action="signup"))

    class Meta:
        model = ContactSubmission
        fields = ["name", "email", "message"]
