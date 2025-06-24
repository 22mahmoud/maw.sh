from django.forms import ValidationError
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from django.utils.translation import gettext_lazy as _

from .constants import SOCIAL_PLATFORMS


class HeadingBlock(blocks.StructBlock):
    heading_text = blocks.CharBlock(classname="title", required=True)
    size = blocks.ChoiceBlock(
        choices=[
            ("", "Select a heading size"),
            ("h1", "H1"),
            ("h2", "H2"),
            ("h3", "H3"),
            ("h4", "H4"),
            ("h5", "H5"),
            ("h6", "H6"),
        ],
        blank=True,
        required=False,
    )

    class Meta:  # type: ignore
        icon = "title"
        template = "blocks/heading_block.html"


def get_available_social_choices():
    return [(value, value["label"]) for _, value in SOCIAL_PLATFORMS.items()]


class SiteSocialLinkBlock(blocks.StructBlock):
    platform = blocks.ChoiceBlock(choices=get_available_social_choices, required=True)

    class Meta:  # type: ignore
        icon = "site"
        label = "Site Social Link"


class LinkStructValue(blocks.StructValue):
    def url(self):
        if self.get("internal_link"):
            return self["internal_link"].url

        if self.get("download_link"):
            return self["download_link"].url

        return self.get("external_link")


class LinkBlock(blocks.StructBlock):
    text = blocks.CharBlock(
        label="Link Title Text",
        required=False,
        help_text=_(
            "Specify title for external link or provide override title for"
            " internal/download/pages links."
        ),
    )

    icon = blocks.CharBlock(required=False, help_text="Optional icon name")
    internal_link = blocks.PageChooserBlock(
        label="Link (Internal Page)",
        required=False,
        help_text=_("Use to link to selected internal page OR..."),
    )

    download_link = DocumentChooserBlock(
        label="Download (Document)",
        required=False,
        help_text=_("Use to link to selected document for download OR"),
    )

    external_link = blocks.URLBlock(
        label="Link (External URL)",
        required=False,
        help_text=_("Use to link to an external site."),
    )

    def clean(self, value):
        result = super().clean(value)

        link_count = sum(
            bool(f)
            for f in [
                result.get("internal_link"),
                result.get("download_link"),
                result.get("external_link"),
            ]
        )

        if link_count == 0:
            raise ValidationError("You must provide one link: page, URL, or document.")

        if link_count > 1:
            raise ValidationError("Only one type of link can be selected.")

        return result

    class Meta:  # type: ignore
        icon = "link"
        label = "Link"
        value_class = LinkStructValue


class SocialLinkStreamBlock(blocks.StreamBlock):
    site = SiteSocialLinkBlock()
    custom = LinkBlock()

    class Meta:  # type: ignore
        label = "Social Links"
        template = "blocks/hero/social_links.html"


class HeroBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=False, help_text="Hero image")
    headline = blocks.CharBlock(required=True, max_length=255)
    text = blocks.RichTextBlock()
    cta = blocks.CharBlock(required=False, max_length=255, default="Contact")
    cta_link = blocks.PageChooserBlock(required=False)
    social_links = SocialLinkStreamBlock(required=False)

    class Meta:  # type: ignore
        template = "blocks/hero/hero_block.html"
        icon = "image"
        label = "Hero Section"
