from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import resolve_url
from django_htmx.http import HttpResponseClientRedirect


class AccountAdapter(DefaultAccountAdapter):
    def respond_email_verification_sent(self, request, user):  # type: ignore
        if request.htmx:
            redirect_url = resolve_url("account_email_verification_sent")
            return HttpResponseClientRedirect(redirect_url)

        return super().respond_email_verification_sent(request, user)

    def post_login(self, request, user, **kwargs):  # type: ignore
        print("post_login")
        if request.htmx:
            response = super().post_login(request, user, **kwargs)
            redirect_url = response["Location"]
            return HttpResponseClientRedirect(redirect_url)

        return super().post_login(request, user, **kwargs)
