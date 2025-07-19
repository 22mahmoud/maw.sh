from wagtail import blocks

from src.contact.forms import ContactForm


class ContactFormStaticBlock(blocks.StaticBlock):
    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)

        if not parent_context:
            return context

        request = parent_context.get("request")
        session = request.session

        form_data = session.pop("contact_form_data", None)
        form_success = session.pop("contact_form_success", None)

        if form_data:
            form = ContactForm(form_data)
            form.is_valid()
        else:
            form = ContactForm()

        context["form"] = form

        if form_success:
            context["success_message"] = form_success

        return context

    class Meta:  # type: ignore
        icon = "form"
        label = "Contact Form"
        template = "blocks/contact_form_block.html"
