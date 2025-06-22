from django.db import models
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel


@register_snippet
class Client(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField(blank=True)
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    featured = models.BooleanField(default=False, help_text="Show in homepage marquee")

    panels = [
        FieldPanel("name"),
        FieldPanel("website"),
        FieldPanel("featured"),
        FieldPanel("logo"),
    ]

    def __str__(self):
        return self.name
