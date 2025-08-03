from allauth.account.forms import AddEmailForm as AllauthAddEmailForm
from allauth.account.forms import ChangePasswordForm as AllauthChangePasswordForm
from allauth.account.forms import LoginForm as AllauthLoginForm
from allauth.account.forms import ResetPasswordForm as AllauthResetPasswordForm
from allauth.account.forms import ResetPasswordKeyForm as AllauthResetPasswordKeyForm
from allauth.account.forms import SetPasswordForm as AllauthSetPasswordForm
from allauth.account.forms import SignupForm as AllauthSignupForm
from django import forms
from django.contrib.auth import get_user_model

from src.base.renderers import FormRenderer

User = get_user_model()


class UserProfileForm(forms.ModelForm):
    default_renderer = FormRenderer()

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "avatar",
        ]
        container_classes = {
            "username": "sm:col-span-2",
            "avatar": "sm:col-span-2 w-fit",
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"autocomplete": "given-name"}),
            "last_name": forms.TextInput(attrs={"autocomplete": "family-name"}),
            "username": forms.TextInput(
                attrs={
                    "autocomplete": "username",
                }
            ),
            "avatar": forms.ClearableFileInput(),
        }


class LoginForm(AllauthLoginForm):
    default_renderer = FormRenderer()


class SignupForm(AllauthSignupForm):
    default_renderer = FormRenderer()


class AddEmailForm(AllauthAddEmailForm):
    default_renderer = FormRenderer()


class ChangePasswordForm(AllauthChangePasswordForm):
    default_renderer = FormRenderer()


class SetPasswordForm(AllauthSetPasswordForm):
    default_renderer = FormRenderer()


class ResetPasswordForm(AllauthResetPasswordForm):
    default_renderer = FormRenderer()


class ResetPasswordKeyForm(AllauthResetPasswordKeyForm):
    default_renderer = FormRenderer()
