from django.db import models
from django.utils.functional import cached_property
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, TabbedInterface, ObjectList
from wagtail.fields import StreamField
from wagtail.contrib.settings.models import register_setting, BaseSiteSetting
from django.utils.translation import gettext_lazy as _
from wagtailmedia.blocks import VideoChooserBlock

from src.seo.models import SeoMetaFields
from .blocks import ClientsMarqueeStaticBlock, HeroBlock, SocialLinkStreamBlock


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
        handles = {
            "twitter": self.twitter,
            "youtube": self.youtube,
            "github": self.github,
            "bluesky": self.bluesky,
            "linkedin": self.linkedin,
            "mastodon": self.fosstodon,
            "pixelfed": self.pixelfed,
        }

        links = {
            "twitter": ("https://x.com/{}", "twitter"),
            "youtube": ("https://youtube.com/@{}", "youtube"),
            "github": ("https://github.com/{}", "github"),
            "bluesky": ("https://bsky.app/profile/{}.bsky.social", "bluesky"),
            "linkedin": ("https://linkedin.com/in/{}", "linkedin"),
            "mastodon": ("https://fosstodon.org/@{}", "mastodon"),
            "pixelfed": ("https://pixelfed.social/{}", "pixelfed"),
        }

        return [
            {
                "url": links[platform][0].format(handle),
                "icon": links[platform][1],
                "platform": platform,
            }
            for platform, handle in handles.items()
            if handle
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
                    FieldPanel("fosstodon"),
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
