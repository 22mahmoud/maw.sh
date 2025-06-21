from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Site


def get_available_social_choices():
    from src.base.models import SiteSettings

    site = Site.objects.get(is_default_site=True)
    settings = SiteSettings.for_site(site)

    return [(item, item["platform"].capitalize()) for item in settings.social_links]


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
