from allauth.account.forms import render_to_string
from allauth.account.views import PasswordResetView as AllAuthPasswordResetView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django_htmx.http import HttpResponseClientRedirect

from .forms import UserProfileForm


class PasswordResetView(AllAuthPasswordResetView):
    def form_valid(self, form):
        response = super().form_valid(form)

        if self.request.htmx and isinstance(response, HttpResponseRedirect):  # type: ignore
            return HttpResponseClientRedirect(response.url)

        return response


password_reset = PasswordResetView.as_view()


class ProfileView(LoginRequiredMixin, FormView):
    template_name = "account/profile.html"
    form_class = UserProfileForm
    success_url = reverse_lazy("account_profile")

    def render_htmx_partial(self, form):
        request = self.request
        context = {
            "form": form,
            "messages": messages.get_messages(request),
        }

        fragments = []
        fragments.append(render_to_string(f"{self.template_name}#profile-form", context, request))
        fragments.append(render_to_string("base.html#messages", context, request))

        return HttpResponse("".join(fragments), content_type="text/html")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Your profile has been updated.")

        if getattr(self.request, "htmx", False):
            form = self.get_form_class()(instance=self.request.user)
            return self.render_htmx_partial(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        if getattr(self.request, "htmx", False):
            return self.render_htmx_partial(form)

        return super().form_invalid(form)
