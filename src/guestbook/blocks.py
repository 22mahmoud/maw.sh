from django.http import HttpRequest
from wagtail import blocks

from .data import guestbook_editor_presets


class GuestbookFormStaticBlock(blocks.StaticBlock):
    def get_context(self, value, parent_context=None):
        from src.guestbook.forms import GuestbookForm

        context = super().get_context(value, parent_context)
        default_preset = guestbook_editor_presets[0]

        if not isinstance((request := context.get("request")), HttpRequest):
            return context

        session = request.session

        form_data = session.pop("guestbook_form_data", None)

        if form_data:
            form = GuestbookForm(form_data)
            form.is_valid()
        else:
            form = GuestbookForm(
                initial={
                    "bg": default_preset["bg"],
                    "text": default_preset["text"],
                    "font": default_preset["font"],
                    "radius": default_preset["radius"],
                    "emoji": default_preset["emoji"],
                }
            )

        context["form"] = form
        context["guestbook_editor_presets"] = guestbook_editor_presets

        return context

    class Meta:  # type: ignore
        icon = "form"
        label = "Guestbook Form"
        template = "blocks/guestbook_form_block.html"
