from django.contrib import messages
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from wagtail.blocks.base import render_to_string
from wagtail.models import Page

from .forms import ContactForm


class ContactView(View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        is_htmx = request.htmx

        if form.is_valid():
            form.save()
            messages.success(self.request, "Message sent! Thanks for reaching out. 🎊")

            if is_htmx:
                context = {
                    "form": ContactForm(),
                    "messages": messages.get_messages(request),
                }

                fragments = []
                fragments.append(render_to_string("partials/contact_form.html", context, request))
                fragments.append(render_to_string("base.html#messages", context, request))

                return HttpResponse("".join(fragments), content_type="text/html")

            page = self.get_page(request)

            return redirect(self.build_redirect_url(request, page))

        if is_htmx:
            return render(request, "partials/contact_form.html", {"form": form})

        page = self.get_page(request)
        page_context = page.get_context(request)
        page_context["form"] = form

        return render(request, page.template, page_context)

    def get_page(self, request):
        page_id = request.POST.get("page_id")
        if not page_id:
            raise Http404("Page not specified")

        try:
            return Page.objects.live().public().get(id=page_id).specific  # type: ignore
        except Page.DoesNotExist:
            raise Http404("Page not found")

    def build_redirect_url(self, request, page):
        redirect_url = page.get_url(request)
        fragment = request.POST.get("source_url_fragment")
        if fragment and fragment.startswith("#"):
            redirect_url += fragment
        return redirect_url
