def get_guestbook_editor_presets():
    from src.guestbook.models import Guestbook

    return [
        {
            "id": "retro",
            "name": "Retro Wave",
            "emoji": "🕹️",
            "styles": Guestbook.STYLE_MAP["retro"],
        },
        {
            "id": "sunset",
            "name": "Sunset Vibes",
            "emoji": "🌅",
            "styles": Guestbook.STYLE_MAP["sunset"],
        },
        {
            "id": "minimal",
            "name": "Minimal",
            "emoji": "🖤",
            "styles": Guestbook.STYLE_MAP["minimal"],
        },
        {
            "id": "bright",
            "name": "Bright Pop",
            "emoji": "🎉",
            "styles": Guestbook.STYLE_MAP["bright"],
        },
    ]
