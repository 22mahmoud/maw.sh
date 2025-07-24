from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page

from .blocks import GuestbookFormStaticBlock


class GuestbookIndexPage(Page):
    intro = RichTextField(
        blank=True, help_text="Optional introduction/help text for the guestbook."
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types = ["guestbook.GuestbookFormPage"]

    def get_context(self, request):
        context = super().get_context(request)
        context["entries"] = Guestbook.objects.filter(
            visibility=Guestbook.Visibility.PUBLIC
        ).order_by("-created_at")

        return context


class GuestbookFormPage(Page):
    intro = RichTextField(
        blank=True, help_text="Optional introduction/help text for the guestbook."
    )

    body = StreamField(
        [
            ("guestbook_form", GuestbookFormStaticBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("body"),
    ]

    parent_page_types = ["guestbook.GuestbookIndexPage"]
    subpage_types = []


class Guestbook(models.Model):
    STYLE_MAP = {
        "retro": "bg-darker text-accent font-mono",
        "sunset": "bg-sunset text-white font-heading",
        "minimal": "bg-dark text-white font-sans",
        "bright": "bg-accent text-black font-sans prose-invert",
    }

    class StylePreset(models.TextChoices):
        RETRO = "retro", "🕹️ Retro Wave"
        SUNSET = "sunset", "🌅 Sunset Vibes"
        MINIMAL = "minimal", "🖤 Minimal"
        BRIGHT = "bright", "🎉 Bright Pop"

    class BorderRadius(models.TextChoices):
        NONE = "rounded-none", "None"
        SLIGHT = "rounded", "Slight"
        LARGE = "rounded-lg", "Large"
        EXTRA = "rounded-xl", "Extra"

    class Visibility(models.TextChoices):
        PUBLIC = "public", "Public"
        PRIVATE = "private", "Private"
        HIDDEN = "hidden", "Hidden"

    name = models.CharField(max_length=100)
    emoji = models.CharField(max_length=2, help_text="Emoji representing mood or vibe")
    message = models.TextField(max_length=200)
    url = models.URLField(blank=True, help_text="Optional link (e.g., social profile, site)")

    visibility = models.CharField(
        max_length=10,
        choices=Visibility.choices,
        default=Visibility.PUBLIC,
        help_text="Control who can view this entry",
    )

    style = models.CharField(
        max_length=20,
        choices=StylePreset.choices,
        default=StylePreset.MINIMAL,
        help_text="Visual style preset for the card",
    )

    radius = models.CharField(
        max_length=20,
        choices=BorderRadius.choices,
        default=BorderRadius.SLIGHT,
        help_text="Border radius of the card",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.emoji} {self.name}"

    def get_style_classes(self):
        return self.STYLE_MAP.get(self.style, "")

    class Meta:
        verbose_name = "Guestbook Entry"
        verbose_name_plural = "Guestbook Entries"
