from django.http import HttpRequest
from wagtail import blocks


class GuestbookFormStaticBlock(blocks.StaticBlock):
    def get_context(self, value, parent_context=None):
        from src.guestbook.forms import GuestbookForm

        context = super().get_context(value, parent_context)

        if not isinstance((request := context.get("request")), HttpRequest):
            return context

        session = request.session

        form_data = session.pop("guestbook_form_data", None)

        if form_data:
            form = GuestbookForm(form_data)
            form.is_valid()
        else:
            form = GuestbookForm()

        context["form"] = form

        return context

    class Meta:  # type: ignore
        icon = "form"
        label = "Guestbook Form"
        template = "blocks/guestbook_form_block.html"
