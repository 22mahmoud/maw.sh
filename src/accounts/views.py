from allauth.account.views import PasswordResetView as AllAuthPasswordResetView
from allauth.socialaccount import providers
from allauth.socialaccount.models import SocialAccount, SocialApp
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django_htmx.http import HttpResponseClientRedirect


class PasswordResetView(AllAuthPasswordResetView):
    def form_valid(self, form):
        response = super().form_valid(form)

        if self.request.htmx and isinstance(response, HttpResponseRedirect):  # type: ignore
            return HttpResponseClientRedirect(response.url)

        return response


password_reset = PasswordResetView.as_view()


def profile_view(request):
    connected_accounts = SocialAccount.objects.filter(user=request.user)

    available_providers = [
        provider
        for provider in providers.registry.get_class_list()
        if SocialApp.objects.filter(provider=provider.id).exists()
    ]

    context = {
        "connected_accounts": connected_accounts,
        "available_providers": available_providers,
    }

    return render(request, "account/profile.html", context)
