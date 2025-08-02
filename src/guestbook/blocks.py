from wagtail import blocks

from .data import get_guestbook_editor_presets


class GuestbookFormStaticBlock(blocks.StaticBlock):
    def get_context(self, value, parent_context=None):
        from src.guestbook.forms import GuestbookForm

        context = super().get_context(value, parent_context)
        guestbook_editor_presets = get_guestbook_editor_presets()
        default_preset = {}
        if len(guestbook_editor_presets):
            default_preset = guestbook_editor_presets[0]

        form = parent_context.get("form") if parent_context else None

        if not form:
            form = GuestbookForm(
                initial={
                    "style": default_preset.get("id", ""),
                    "emoji": default_preset.get("emoji", ""),
                    "radius": default_preset.get("radius", ""),
                }
            )

        context["form"] = form
        context["guestbook_editor_presets"] = guestbook_editor_presets

        return context

    class Meta:  # type: ignore
        icon = "form"
        label = "Guestbook Form"
        template = "blocks/guestbook_form_block.html"
