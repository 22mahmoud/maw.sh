from django.db import models
from django.utils.functional import cached_property
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, TabbedInterface, ObjectList
from wagtail.fields import StreamField
from wagtail.contrib.settings.models import register_setting, BaseSiteSetting
from django.utils.translation import gettext_lazy as _
from wagtailmedia.blocks import VideoChooserBlock

from src.seo.models import SeoMetaFields
from src.clients.blocks import ClientsMarqueeStaticBlock
from .blocks import HeroBlock, SocialLinkStreamBlock
from .constants import SOCIAL_PLATFORMS


class GenericPage(SeoMetaFields, Page):  # type: ignore
    introduction = models.TextField(help_text="Text to describe the page", blank=True)

    body = StreamField(
        [
            ("hero", HeroBlock()),
            ("clients", ClientsMarqueeStaticBlock()),
            ("social_links", SocialLinkStreamBlock()),
            ("Video", VideoChooserBlock()),
        ],
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

    mastodon = models.CharField(
        blank=True,
        verbose_name=_("Mastodon"),
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

    linkedin = models.CharField(
        blank=True,
        verbose_name=_("Linkedin"),
    )

    bluesky = models.CharField(
        blank=True,
        verbose_name=_("Bluesky"),
    )

    @cached_property
    def social_links(self):
        return [
            {
                "text": SOCIAL_PLATFORMS[key]["label"],
                "url": SOCIAL_PLATFORMS[key]["url_pattern"].format(getattr(self, key)),
                "icon": SOCIAL_PLATFORMS[key]["icon"],
                "platform": key,
            }
            for key in SOCIAL_PLATFORMS
            if getattr(self, key)
        ]

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
                    FieldPanel("mastodon"),
                    FieldPanel("bluesky"),
                    FieldPanel("pixelfed"),
                    FieldPanel("youtube"),
                    FieldPanel("reddit"),
                    FieldPanel("github"),
                    FieldPanel("linkedin"),
                ],
                heading="Social Media",
            ),
        ]
    )
