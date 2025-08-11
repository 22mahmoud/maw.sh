from django.db import models
from taggit.models import TaggedItemBase
from wagtail.models import ParentalKey


class PageTag(TaggedItemBase):
    content_object = ParentalKey(
        "wagtailcore.Page",
        related_name="tagged_items",
        on_delete=models.CASCADE,
    )
