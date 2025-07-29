from allauth.account.views import PasswordResetView as AllAuthPasswordResetView
from django.contrib.auth.decorators import login_required
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


@login_required
def profile_view(request):
    return render(
        request,
        "account/profile.html",
    )
