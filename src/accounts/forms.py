from allauth.account.forms import AddEmailForm as AllauthAddEmailForm
from allauth.account.forms import ChangePasswordForm as AllauthChangePasswordForm
from allauth.account.forms import LoginForm as AllauthLoginForm
from allauth.account.forms import ResetPasswordForm as AllauthResetPasswordForm
from allauth.account.forms import ResetPasswordKeyForm as AllauthResetPasswordKeyForm
from allauth.account.forms import SetPasswordForm as AllauthSetPasswordForm
from allauth.account.forms import SignupForm as AllauthSignupForm
from django import forms
from django.contrib.auth import get_user_model
from wagtail.images import get_image_model
from wagtail.models import Collection

from src.base.renderers import FormRenderer

User = get_user_model()
ImageModel = get_image_model()


class UserProfileForm(forms.ModelForm):
    default_renderer = FormRenderer()

    avatar = forms.FileField(required=False, widget=forms.ClearableFileInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.avatar:
            self.fields["avatar"].initial = self.instance.avatar.file

    def save(self, commit=True):
        user = super().save(commit=False)
        existing_avatar = user.avatar
        avatar_file = self.files.get("avatar")

        if not self.cleaned_data["avatar"] and existing_avatar:
            user.avatar = None
            existing_avatar.delete()

        if avatar_file:
            collection = Collection.objects.get(name="avatars")
            image = ImageModel(
                title=f"{user.username} Avatar",
                file=avatar_file,
                collection=collection,
            )

            image.save()

            user.avatar = image
            if existing_avatar:
                existing_avatar.delete()

        if commit:
            user.save()

        return user

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
        ]
        container_classes = {
            "username": "sm:col-span-2",
            "avatar": "sm:col-span-2 w-fit",
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"autocomplete": "given-name"}),
            "last_name": forms.TextInput(attrs={"autocomplete": "family-name"}),
            "username": forms.TextInput(attrs={"autocomplete": "username"}),
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
