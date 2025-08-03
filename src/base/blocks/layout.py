from wagtail import blocks

from src.base.blocks.button import ButtonBlock
from src.base.blocks.feed import FeaturedBlogBlock, FeedBlock
from src.base.blocks.hero import HeroBlock
from src.base.blocks.link import LinkBlock, SiteSocialLinkBlock


class SpacerBlock(blocks.StructBlock):
    size = blocks.ChoiceBlock(
        choices=[
            ("sm", "Small"),
            ("md", "Medium"),
            ("lg", "Large"),
            ("xl", "Extra Large"),
        ],
        default="md",
        label="Spacer Size",
        help_text="Select a predefined amount of vertical space to add.",
    )

    class Meta:  # type: ignore
        template = "blocks/spacer_block.html"
        icon = "arrows-up-down"
        label = "Preset Spacer"


class FlexLayoutBlock(blocks.StructBlock):
    gap = blocks.ChoiceBlock(
        choices=[
            ("gap-2", "Small"),
            ("gap-4", "Medium"),
            ("gap-6", "Large"),
            ("gap-8", "Extra Large"),
        ],
        default="gap-4",
        label="Gap between items",
    )

    responsive = blocks.ChoiceBlock(
        help_text=(
            "Choose the breakpoint where items switch from "
            "stacked (vertical) to inline (horizontal)."
        ),
        choices=[
            ("sm", "Stack < 640 px (sm)"),
            ("md", "Stack < 768 px (md)"),
            ("lg", "Stack < 1024 px (lg)"),
            ("xl", "Never stack – always row"),
        ],
        default="sm",
        label="Responsive behaviour",
    )

    horizontal_align = blocks.ChoiceBlock(
        required=False,
        choices=[
            ("start", "Left/Start"),
            ("center", "Center"),
            ("end", "Right/End"),
            ("between", "Space Between"),
            ("around", "Space Around"),
            ("evenly", "Space Evenly"),
        ],
        label="Horizontal alignment",
    )

    vertical_align = blocks.ChoiceBlock(
        required=False,
        choices=[
            ("start", "Top/Start"),
            ("center", "Center"),
            ("end", "Bottom/End"),
            ("stretch", "Stretch"),
        ],
        label="Vertical alignment",
    )

    extra_class = blocks.CharBlock(
        required=False,
        label="Additional CSS classes",
        help_text="For design‑system power users. Space‑separated list, no leading dot.",
    )

    content = blocks.StreamBlock(
        [
            ("link", LinkBlock()),
            ("social", SiteSocialLinkBlock()),
            ("button", ButtonBlock()),
            ("hero", HeroBlock()),
            ("featured_blog", FeaturedBlogBlock()),
            ("feed", FeedBlock()),
        ],
        label="Child blocks",
    )

    class Meta:  # type: ignore
        template = "blocks/flex_layout_block.html"
        icon = "group"
