from django.http import HttpRequest
from wagtail import blocks

guestbook_editor_presets = [
    {
        "name": "Retro Wave",
        "bg": "bg-darker",
        "text": "text-accent",
        "font": "font-mono",
        "radius": "rounded",
        "emoji": "🕹️",
    },
    {
        "name": "Sunset Vibes",
        "bg": "bg-sunset",
        "text": "text-white",
        "font": "font-serif",
        "radius": "rounded-xl",
        "emoji": "🌅",
    },
    {
        "name": "Minimal",
        "bg": "bg-dark",
        "text": "text-white",
        "font": "font-sans",
        "radius": "rounded-lg",
        "emoji": "🖤",
    },
    {
        "name": "Bright Pop",
        "bg": "bg-accent",
        "text": "text-black",
        "font": "font-sans",
        "radius": "rounded-3xl",
        "emoji": "🎉",
    },
    {
        "name": "Calm Forest",
        "bg": "bg-gradient-1",
        "text": "text-white",
        "font": "font-serif",
        "radius": "rounded-xl",
        "emoji": "🌲",
    },
    {
        "name": "Golden Hour",
        "bg": "bg-gradient-2",
        "text": "text-black",
        "font": "font-sans",
        "radius": "rounded-lg",
        "emoji": "🌞",
    },
    {
        "name": "Night Neon",
        "bg": "bg-darker",
        "text": "text-accent",
        "font": "font-mono",
        "radius": "rounded-xl",
        "emoji": "🌌",
    },
]


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
            form = GuestbookForm(
                initial={
                    "bg": guestbook_editor_presets[0]["bg"],
                    "text": guestbook_editor_presets[0]["text"],
                    "font": guestbook_editor_presets[0]["font"],
                    "radius": guestbook_editor_presets[0]["radius"],
                    "emoji": guestbook_editor_presets[0]["emoji"],
                }
            )

        context["form"] = form
        context["guestbook_editor_presets"] = guestbook_editor_presets

        return context

    class Meta:  # type: ignore
        icon = "form"
        label = "Guestbook Form"
        template = "blocks/guestbook_form_block.html"
