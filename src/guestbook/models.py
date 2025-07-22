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
    class BackgroundStyle(models.TextChoices):
        WHITE = "bg-white", "White"
        SUNSET = "bg-sunset", "Sunset"
        GREEN = "bg-gradient-1", "Green"
        YELLOW = "bg-gradient-2", "Yellow"
        ACCENT = "bg-accent", "Accent"
        DARKER = "bg-darker", "Dark"

    class TextColor(models.TextChoices):
        BLACK = "text-black", "Black"
        WHITE = "text-white", "White"
        ACCENT = "text-accent", "Accent"

    class FontStyle(models.TextChoices):
        SANS = "font-sans", "Sans"
        HEADING = "font-heading", "Heading"
        MONO = "font-mono", "Mono"

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
    message = models.TextField()
    url = models.URLField(
        blank=True, help_text="Optional link (e.g., social profile, site)"
    )

    visibility = models.CharField(
        max_length=10,
        choices=Visibility.choices,
        default=Visibility.PUBLIC,
        help_text="Control who can view this entry",
    )

    bg = models.CharField(
        max_length=50, choices=BackgroundStyle.choices, default=BackgroundStyle.WHITE
    )

    text = models.CharField(
        max_length=50, choices=TextColor.choices, default=TextColor.BLACK
    )

    font = models.CharField(
        max_length=50, choices=FontStyle.choices, default=FontStyle.SANS
    )

    radius = models.CharField(
        max_length=50, choices=BorderRadius.choices, default=BorderRadius.SLIGHT
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.emoji} {self.name}"

    class Meta:
        verbose_name = "Guestbook Entry"
        verbose_name_plural = "Guestbook Entries"
