from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "avatar",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"autocomplete": "given-name"}),
            "last_name": forms.TextInput(attrs={"autocomplete": "family-name"}),
            "username": forms.TextInput(
                attrs={
                    "autocomplete": "username",
                    "container_class": "sm:col-span-2",
                }
            ),
            "avatar": forms.ClearableFileInput(
                attrs={
                    "container_class": "sm:col-span-2 w-fit",
                }
            ),
        }
