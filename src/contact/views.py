from django.http import Http404, HttpResponseBadRequest
from django.views import View
from django.template.response import TemplateResponse
from django.shortcuts import redirect, render
from wagtail.models import Page


from .forms import ContactForm


class ContactView(View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        is_htmx = request.htmx

        if form.is_valid():
            form.save()
            success_message = "Message sent! Thanks for reaching out. 🎊"
            request.session["contact_form_success"] = success_message

            context = {
                "form": ContactForm(),
                "success_message": success_message,
            }

            if is_htmx:
                return render(request, "partials/contact_form.html", context)

            page = self.get_page(request)
            return redirect(self.build_redirect_url(request, page))

        request.session["contact_form_data"] = request.POST.copy()
        context = {"form": form}

        if is_htmx:
            return render(request, "partials/contact_form.html", context)

        page = self.get_page(request)
        return redirect(self.build_redirect_url(request, page))

    def get_page(self, request):
        page_id = request.POST.get("page_id")
        if not page_id:
            raise Http404("Page not specified")

        try:
            return Page.objects.live().public().get(id=page_id).get_specific()  # type: ignore
        except Page.DoesNotExist:
            raise Http404("Page not found")

    def build_redirect_url(self, request, page):
        redirect_url = page.get_url(request)
        fragment = request.POST.get("source_url_fragment")
        if fragment and fragment.startswith("#"):
            redirect_url += fragment
        return redirect_url


def validate_contact_field(request):
    if request.method != "POST" or not request.headers.get("HX-Request"):
        return HttpResponseBadRequest("Invalid request")

    triggering_element_id = request.htmx.trigger
    if not triggering_element_id:
        return HttpResponseBadRequest("Missing trigger ID in htmx request.")

    field_name = triggering_element_id.removesuffix("-wrapper")

    form = ContactForm(request.POST)
    form.is_valid()

    if field_name not in form.fields:
        return HttpResponseBadRequest("Invalid field name derived from trigger.")

    template_fragment_name = field_name

    return TemplateResponse(
        request,
        f"partials/contact_form.html#{template_fragment_name}",
        {"form": form},
    )
