from django.contrib import admin

from .models import Guestbook


@admin.register(Guestbook)
class GuestbookAdmin(admin.ModelAdmin):
    list_display = ("name", "emoji", "visibility", "style", "radius", "created_at")
    list_filter = ("visibility", "style", "radius", "created_at")
    search_fields = ("name", "message", "url")
    readonly_fields = ("created_at", "message_html")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "emoji",
                    "message",
                    "message_html",
                    "url",
                    "pinned",
                )
            },
        ),
        (
            "Display Settings",
            {
                "fields": (
                    "visibility",
                    "style",
                    "radius",
                )
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at",),
            },
        ),
    )
