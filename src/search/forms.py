from django import forms

from src.base.renderers import FormRenderer


class SearchForm(forms.Form):
    default_renderer = FormRenderer()

    q = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "type": "search",
                "placeholder": "Search...",
                "aria-label": "Search",
                "autocomplete": "search",
            }
        ),
    )
