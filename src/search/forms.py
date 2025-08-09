from django import forms

from src.base.renderers import FormRenderer


class SearchForm(forms.Form):
    default_renderer = FormRenderer()

    q = forms.CharField(
        required=False,
        label="",
        widget=forms.widgets.SearchInput(  # type: ignore
            attrs={
                "placeholder": "Search...",
                "aria-label": "Search",
                "autocomplete": "search",
            }
        ),
    )
