from allauth.socialaccount import providers
from allauth.socialaccount.models import SocialAccount, SocialApp
from django.shortcuts import render


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
