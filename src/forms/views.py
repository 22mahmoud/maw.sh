from django.http import HttpResponseNotAllowed
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

        response = render(request, "partials/contact_form.html", context)

        return response
    else:
        context = {"form": form}
        response = render(request, "partials/contact_form.html", context)

        return response
