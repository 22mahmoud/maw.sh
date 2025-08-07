from wagtail import blocks


class ContactFormStaticBlock(blocks.StaticBlock):
    pass


class ContactFormBlock(blocks.StructBlock):
    heading = blocks.CharBlock(
        required=False,
        default="Let’s Connect 👋",
        help_text="Main heading for the contact form section",
    )

    description = blocks.TextBlock(
        required=False,
        default="Prefer typing over talking? Drop me a line below — I’ll get back to you shortly.",
        help_text="Introductory text for the contact form section",
    )

    show_container = blocks.BooleanBlock(
        required=False,
        default=True,
        help_text="Wrap the form section with outer padding & zigzag container",
    )

    def get_context(self, value, parent_context=None):
        from src.contact.forms import ContactForm

        context = super().get_context(value, parent_context)

        form = parent_context.get("form") if parent_context else None

        if not form:
            form = ContactForm()

        context["form"] = form
        context["heading"] = value.get("heading")
        context["description"] = value.get("description")
        context["show_container"] = value.get("show_container")

        return context

    class Meta:  # type: ignore
        icon = "form"
        label = "Contact Form"
        template = "blocks/contact_form_block.html"
