from django.conf import settings
from wagtail import blocks

from src.forms.forms import ContactForm


class ContactFormStaticBlock(blocks.StaticBlock):
    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context["form"] = ContactForm()
        context["RECAPTCHA_SITE_KEY"] = settings.RECAPTCHA_PUBLIC_KEY
        return context

    class Meta:  # type: ignore
        icon = "form"
        label = "Contact Form"
        template = "blocks/contact_form_block.html"
