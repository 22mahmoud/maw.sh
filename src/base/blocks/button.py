from wagtail import blocks
from wagtail.documents.blocks import DocumentChooserBlock

from .link import LinkStructValue

BUTTON_TYPE_CHOICES = (
    ("primary", "Primary"),
    ("secondary", "Secondary"),
    ("outline", "Outline"),
    ("muted", "Muted"),
    ("disabled", "Disabled"),
)

DEFAULT_BUTTON_TYPE = "primary"

BUTTON_SIZE_CHOICES = (
    ("sm", "Small"),
    ("md", "Medium"),
    ("lg", "Large"),
)

DEFAULT_BUTTON_SIZE = "md"


class ButtonStructValue(LinkStructValue):
    pass


class ButtonBlock(blocks.StructBlock):
    type = blocks.ChoiceBlock(choices=BUTTON_TYPE_CHOICES, default=DEFAULT_BUTTON_TYPE)
    size = blocks.ChoiceBlock(choices=BUTTON_SIZE_CHOICES, default=DEFAULT_BUTTON_SIZE)

    prefix_icon_name = blocks.CharBlock(
        required=False,
        label="Prefix Icon",
        help_text="Icon to display before the text.",
    )
    suffix_icon_name = blocks.CharBlock(
        required=False, label="Suffix Icon", help_text="Icon to display after the text."
    )
    icon_name = blocks.CharBlock(
        required=False,
        label="Icon-Only",
        help_text="For an icon-only button. Overrides prefix/suffix icons.",
    )

    text = blocks.CharBlock(max_length=20)

    external_link = blocks.URLBlock(required=False)
    internal_link = blocks.PageChooserBlock(required=False)
    download_link = DocumentChooserBlock(required=False)

    class Meta:  # type: ignore
        icon = "plus-inverse"
        template = "blocks/button_block.html"
        value_class = ButtonStructValue
