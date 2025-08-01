from django import forms


class SearchForm(forms.Form):
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
