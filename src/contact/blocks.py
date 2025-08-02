from wagtail import blocks

from src.contact.forms import ContactForm


class ContactFormStaticBlock(blocks.StaticBlock):
    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)

        form = parent_context.get("form") if parent_context else None

        if not form:
            form = ContactForm()

        context["form"] = form

        return context

    class Meta:  # type: ignore
        icon = "form"
        label = "Contact Form"
        template = "blocks/contact_form_block.html"
