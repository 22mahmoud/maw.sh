from django import forms
from django_comments_xtd.forms import XtdCommentForm as DjangoXtdCommentForm

from src.base.renderers import FormRenderer


class XtdCommentForm(DjangoXtdCommentForm):
    default_renderer = FormRenderer()
    phone = forms.CharField(
        required=False,
        label="Phone number",
        widget=forms.widgets.TelInput(  # type: ignore
            attrs={
                "autocomplete": "tel",
                "placeholder": "Your phone number",
                "tabindex": "-1",
                "style": "position:absolute; left:-9999px;",
                "aria-hidden": "true",
            }
        ),
    )

    def clean_phone(self):
        value = self.cleaned_data["phone"]
        if value:
            raise forms.ValidationError("error")
        return value

    def security_errors(self):
        errors = super().security_errors()

        for f in ["phone"]:
            if f in self.errors:
                errors[f] = self.errors[f]

        return errors
