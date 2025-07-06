from wagtail import blocks
from wagtail.documents.blocks import DocumentChooserBlock

from src.utils.cva import cva

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

BUTTON_CVA = cva(
    base=(
        "group relative inline-block cursor-pointer shadow-xs focus-visible:outline-2 "
        "focus-visible:outline-offset-2 focus-visible:outline-accent-bright"
    ),
    variants={
        "variant": {
            "primary": "text-darker font-bold",
            "secondary": "bg-neutral-800 text-primary hover:bg-neutral-700 font-medium",
            "outline": (
                "border-2 border-accent-bright text-primary bg-transparent "
                "transition-colors duration-200 hover:bg-accent-bright hover:text-black"
            ),
            "muted": (
                "text-neutral-300 hover:text-primary hover:bg-neutral-800 "
                "border border-neutral-700 hover:border-neutral-500 font-medium "
                "transition-colors duration-200"
            ),
            "disabled": (
                "bg-neutral-800 text-secondary border border-neutral-700 "
                "opacity-50 cursor-not-allowed pointer-events-none"
            ),
        },
        "size": {
            "sm": "text-sm px-2 py-1 sm:px-3 sm:py-1.5",
            "md": "text-base px-3 py-1.5 sm:px-4 sm:py-2",
            "lg": "text-lg sm:text-2xl px-3 py-2 sm:px-4 sm:py-2.5",
        },
    },
    default_variants={
        "variant": "primary",
        "size": "md",
    },
)

BUTTON_ICON_CVA = cva(
    base="",
    variants={
        "variant": {
            "primary": "fill-darker",
            "secondary": "fill-primary",
            "outline": "fill-primary group-hover:fill-black",
            "muted": "fill-neutral-300 group-hover:fill-primary",
            "disabled": "fill-secondary",
        },
        "size": {
            "sm": "w-6 h-6",
            "md": "w-5 h-5",
            "lg": "w-4 h-4",
        },
    },
    default_variants={
        "variant": "primary",
        "size": "md",
    },
)

BUTTON_TEXT_CVA = cva(
    base="",
    variants={
        "variant": {
            "primary": "",
            "secondary": "font-medium",
            "outline": "font-normal sm:font-semibold",
            "muted": "font-medium",
            "disabled": "text-secondary",
        },
        "size": {
            "sm": "text-sm",
            "md": "text-base",
            "lg": "text-lg",
        },
    },
    default_variants={
        "variant": "primary",
        "size": "md",
    },
)


class ButtonStructValue(LinkStructValue):
    def is_link(self):
        return bool(self.url()) and self.get("button_type") != "disabled"

    def wrapper_tag(self):
        return "a" if self.is_link() else "button"

    def wrapper_attrs(self):
        if self.is_link():
            return f"href={self.url()} role=link"
        elif self.get("button_type") == "disabled":
            return 'type="button" role="button" disabled'
        return 'type="button" role="button"'

    def props(self):
        type_ = self.get("button_type", "primary")
        size = self.get("size", "lg")
        return {
            "variant": type_,
            "size": size,
        }


class ButtonBlock(blocks.StructBlock):
    button_type = blocks.ChoiceBlock(
        choices=BUTTON_TYPE_CHOICES, default=DEFAULT_BUTTON_TYPE
    )
    size = blocks.ChoiceBlock(choices=BUTTON_SIZE_CHOICES, default=DEFAULT_BUTTON_SIZE)
    button_icon = blocks.CharBlock(required=False, help_text="Optional icon name")
    button_text = blocks.CharBlock(max_length=20)
    external_link = blocks.URLBlock(required=False)
    internal_link = blocks.PageChooserBlock(required=False)
    download_link = DocumentChooserBlock(required=False)

    class Meta:  # type: ignore
        icon = "plus-inverse"
        template = "blocks/button_block.html"
        value_class = ButtonStructValue


def get_cva(name):
    return {
        "button": BUTTON_CVA,
        "button_icon": BUTTON_ICON_CVA,
        "button_text": BUTTON_TEXT_CVA,
    }.get(name)
