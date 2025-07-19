from django.http import HttpResponseBadRequest, HttpResponseNotAllowed
from django.template.response import TemplateResponse
from django.shortcuts import render

from .forms import ContactForm


def contact(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    form = ContactForm(request.POST)

    if form.is_valid():
        form.save()
        context = {
            "form": ContactForm(),
            "success_message": "Message sent! Thanks for reaching out. 🎊",
        }

    else:
        context = {"form": form}

    return render(request, "partials/contact_form.html", context)


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
