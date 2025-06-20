from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.contrib.settings.models import register_setting, BaseSiteSetting
from wagtail.admin.panels import FieldPanel, TabbedInterface, ObjectList
from wagtail.admin.panels import MultiFieldPanel
from wagtail.models import Page


class SeoMetaFields(Page):
    class Meta:  # type: ignore
        abstract = True

    canonical_url = models.URLField(
        blank=True,
        max_length=255,
        verbose_name=_("Canonical URL"),
        help_text=_("Leave blank to use the page's URL."),
    )

    og_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Preview image"),
        help_text=_(
            "Shown when linking to this page on social media. "
            "If blank, may show an image from the page, "
            "or the default from Settings > SEO."
        ),
    )

    @property
    def seo_canonical_url(self) -> str:
        return self.canonical_url or self.get_full_url() or ""

    promote_panels = Page.promote_panels + [
        MultiFieldPanel(
            [
                FieldPanel("canonical_url"),
                FieldPanel("og_image"),
            ],
            _("Search and Social Previews"),
        ),
    ]


@register_setting(icon="globe")
class SeoSettings(BaseSiteSetting):
    title_suffix = models.CharField(
        verbose_name="Title suffix",
        max_length=255,
        help_text="The suffix for the title meta tag e.g. ' | The Wagtail Bakery'",
        default="Mahmoud Ashraf",
    )

    og_image_default = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Default preview image"),
        help_text=_(
            "Shown when linking to this page on social media. "
            "This can also be customized on each page."
        ),
    )

    edit_handler = TabbedInterface(
        [
            ObjectList(
                [FieldPanel("title_suffix"), FieldPanel("og_image_default")],
                heading="SEO",
            ),
        ]
    )
