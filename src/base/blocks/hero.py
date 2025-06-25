from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from .button import ButtonBlock
from .link import SocialLinkStreamBlock


class HeroBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=False, help_text="Hero image")
    headline = blocks.CharBlock(required=True, max_length=255)
    text = blocks.RichTextBlock(features=["bold", "italic", "link"])
    cta = ButtonBlock()
    social_links = SocialLinkStreamBlock(required=False)

    class Meta:  # type: ignore
        template = "blocks/hero/hero_block.html"
        icon = "image"
        label = "Hero Section"
