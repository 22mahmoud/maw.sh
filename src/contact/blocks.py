from wagtail import blocks


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

    TYPE_CHOICES = [
        ("section", "Full Section (with heading, description & container)"),
        ("form", "Just Form (simple padded block)"),
    ]

    type = blocks.ChoiceBlock(
        choices=TYPE_CHOICES,
        default="section",
        help_text="Choose whether to display as a full section or just the form",
    )

    def get_context(self, value, parent_context=None):
        from src.contact.forms import ContactForm

        context = super().get_context(value, parent_context)

        form = parent_context.get("form") if parent_context else None

        if not form:
            form = ContactForm()

        context.update(
            {
                "form": form,
                "type": value.get("type"),
                "heading": value.get("heading"),
                "description": value.get("description"),
            }
        )

        return context

    class Meta:  # type: ignore
        icon = "form"
        label = "Contact Form"
        template = "blocks/contact_form_block.html"


class DummyDeprecatedContactFormStaticBlock(blocks.StaticBlock):
    class Meta:  # type: ignore
        label = "Deprecated DummyDeprecatedContactFormStaticBlock (Ignored)"
