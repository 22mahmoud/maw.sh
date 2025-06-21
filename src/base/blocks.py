from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class HeroBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=False, help_text="Hero image")
    headline = blocks.CharBlock(required=True, max_length=255)
    text = blocks.RichTextBlock()
    cta = blocks.CharBlock(required=False, max_length=255, default="Contact")
    cta_link = blocks.PageChooserBlock(required=False)

    class Meta:  # type: ignore
        template = "blocks/hero/hero_block.html"
        icon = "image"
        label = "Hero Section"
