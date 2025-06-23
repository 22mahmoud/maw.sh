from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

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


class CustomSocialLinkBlock(blocks.StructBlock):
    platform = blocks.CharBlock(
        required=True,
        help_text="Name of the platform or icon (e.g. 'reddit', 'discord')",
    )

    url = blocks.URLBlock(required=True)

    class Meta:  # type: ignore
        icon = "link"
        label = "Custom Social Link"


class SocialLinkStreamBlock(blocks.StreamBlock):
    site = SiteSocialLinkBlock()
    custom = CustomSocialLinkBlock()

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
