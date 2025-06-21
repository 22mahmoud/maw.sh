from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, TabbedInterface, ObjectList
from wagtail.fields import StreamField
from wagtail.contrib.settings.models import register_setting, BaseSiteSetting
from django.utils.translation import gettext_lazy as _

from src.seo.models import SeoMetaFields
from .blocks import HeroBlock


class GenericPage(SeoMetaFields, Page):  # type: ignore
    introduction = models.TextField(help_text="Text to describe the page", blank=True)

    body = StreamField(
        [("hero", HeroBlock())],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("body"),
    ]


@register_setting(icon="site")
class SiteSettings(BaseSiteSetting):
    avilable_for_projects = models.BooleanField(
        verbose_name=_("Avilable for projects"), default=False
    )

    twitter = models.CharField(
        blank=True,
        verbose_name=_("Twitter"),
    )

    fosstodon = models.CharField(
        blank=True,
        verbose_name=_("Fosstodon"),
    )

    youtube = models.CharField(
        blank=True,
        verbose_name=_("Youtube"),
    )

    reddit = models.CharField(
        blank=True,
        verbose_name=_("Reddit"),
    )

    github = models.CharField(
        blank=True,
        verbose_name=_("Github"),
    )

    pixelfed = models.CharField(
        blank=True,
        verbose_name=_("Pixelfed.social"),
    )

    bluesky = models.CharField(
        blank=True,
        verbose_name=_("Bluesky"),
    )

    edit_handler = TabbedInterface(
        [
            ObjectList(
                [
                    FieldPanel("avilable_for_projects"),
                ],
                heading="General",
            ),
            ObjectList(
                [
                    FieldPanel("twitter"),
                    FieldPanel("fosstodon"),
                    FieldPanel("bluesky"),
                    FieldPanel("pixelfed"),
                    FieldPanel("youtube"),
                    FieldPanel("reddit"),
                    FieldPanel("github"),
                ],
                heading="Social Media",
            ),
        ]
    )
