from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtailmedia.blocks import VideoChooserBlock

from src.base.blocks.button import ButtonBlock
from src.base.blocks.hero import HeroBlock
from src.base.blocks.link import SocialLinkStreamBlock
from src.clients.blocks import ClientsMarqueeStaticBlock
from src.seo.models import SeoMetaFields


class HomePage(RoutablePageMixin, SeoMetaFields, Page):  # type: ignore
    introduction = models.TextField(help_text="Text to describe the page", blank=True)
    POSTS_PER_PAGE = 1

    template = "base/generic_page.html"

    body = StreamField(
        [
            ("hero", HeroBlock()),
            ("clients", ClientsMarqueeStaticBlock()),
            ("social_links", SocialLinkStreamBlock()),
            ("Video", VideoChooserBlock()),
            ("button", ButtonBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("body"),
    ]
