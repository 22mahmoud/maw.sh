from captcha.fields import CaptchaField, CaptchaTextInput
from django import forms

from .models import ContactSubmission


class CustomCaptchaTextInput(CaptchaTextInput):
    template_name = "includes/custom_captcha_field.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["errors"] = self.attrs.get("errors", None)

        return context


class ContactForm(forms.ModelForm):
    captcha = CaptchaField(widget=CustomCaptchaTextInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.is_bound and self.errors.get("captcha"):
            errors = self.errors["captcha"]
            self.fields["captcha"].widget.attrs["errors"] = errors

    class Meta:
        model = ContactSubmission
        fields = ["name", "email", "message", "captcha"]
