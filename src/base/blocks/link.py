from django.utils.translation import gettext_lazy as _
from django.forms import ValidationError
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail import blocks

from src.base.constants import SOCIAL_PLATFORMS
from src.utils.cva import cva

LINK_CVA = cva(
    base=(
        "inline-flex items-center gap-3 group focus-visible:outline-none focus-visible:ring "
        "focus-visible:ring-primary underline-offset-4 hover:underline"
    ),
    variants={
        "variant": {
            "default": "text-primary hover:text-accent",
            "icon": "text-primary hover:text-accent",
            "nav": "text-white hover:text-accent",
            "nav_active": "text-accent",
        },
        "size": {
            "sm": "text-sm",
            "md": "text-base",
            "lg": "text-lg",
        },
    },
    default_variants={
        "variant": "default",
        "size": "md",
    },
)

LINK_ICON_CVA = cva(
    base="transition-colors",
    variants={
        "variant": {
            "default": "fill-primary group-hover:fill-accent",
            "icon": "fill-primary group-hover:fill-accent",
            "nav": "fill-white group-hover:fill-accent",
            "nav_active": "fill-accent",
        },
        "size": {
            "sm": "w-4 h-4",
            "md": "w-6 h-6",
            "lg": "w-8 h-8",
        },
    },
    default_variants={
        "variant": "default",
        "size": "md",
    },
)

LINK_TEXT_CVA = cva(
    base="transition-colors",
    variants={
        "variant": {
            "default": "text-primary hover:text-accent",
            "icon": "text-primary hover:text-accent",
            "nav": "text-white group-hover:text-accent",
            "nav_active": "text-accent",
        },
        "size": {
            "sm": "text-sm",
            "md": "text-base",
            "lg": "text-lg",
        },
    },
    default_variants={
        "variant": "default",
        "size": "md",
    },
)


class LinkStructValue(blocks.StructValue):
    def url(self):
        if self.get("internal_link"):
            return self["internal_link"].url

        if self.get("download_link"):
            return self["download_link"].url

        return self.get("external_link")

    def is_icon_only(self):
        return bool(self.get("icon")) and not bool(self.get("text"))

    def props(self):
        return {
            "variant": self.get("link_type", "default"),
            "size": self.get("size", "md"),
        }


class LinkBlock(blocks.StructBlock):
    link_type = blocks.ChoiceBlock(
        choices=[
            ("default", "Default Link"),
            ("icon", "Icon Only"),
        ],
        default="default",
        required=False,
    )

    size = blocks.ChoiceBlock(
        choices=[
            ("sm", "Small"),
            ("md", "Medium"),
            ("lg", "Large"),
        ],
        default="md",
        required=False,
    )

    text = blocks.CharBlock(
        label="Link Title Text",
        required=False,
        help_text=_(
            "Specify title for external link or provide override title for"
            " internal/download/pages links."
        ),
    )
    sr_text = blocks.CharBlock(
        label="Screen Reader Link Text",
        required=False,
        help_text=_("Specify title for screen Reader in case you use only icons"),
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
        links = [
            result.get("internal_link"),
            result.get("download_link"),
            result.get("external_link"),
        ]

        if sum(bool(link) for link in links) != 1:
            raise ValidationError(
                "Provide exactly one of internal, download, or external link."
            )
        return result

    class Meta:  # type: ignore
        icon = "link"
        label = "Link"
        value_class = LinkStructValue
        template = "blocks/link_block.html"


class SiteSocialStructValue(blocks.StructValue):
    def props(self):
        return {
            "variant": "icon",
            "size": self.get("size", "md"),
        }


def get_available_social_choices():
    return [(key, value["label"]) for key, value in SOCIAL_PLATFORMS.items()]


class SiteSocialLinkBlock(blocks.StructBlock):
    platform = blocks.ChoiceBlock(choices=get_available_social_choices, required=True)
    size = blocks.ChoiceBlock(
        choices=[
            ("sm", "Small"),
            ("md", "Medium"),
            ("lg", "Large"),
        ],
        default="md",
        required=False,
    )

    class Meta:  # type: ignore
        icon = "site"
        label = "Site Social Link"
        value_class = SiteSocialStructValue
        template = "blocks/link_block.html"


class SocialLinkStreamBlock(blocks.StreamBlock):
    site = SiteSocialLinkBlock()
    custom = LinkBlock()

    class Meta:  # type: ignore
        label = "Social Links"
        template = "blocks/social_links.html"


def get_cva(name):
    return {
        "link": LINK_CVA,
        "link_icon": LINK_ICON_CVA,
        "link_text": LINK_TEXT_CVA,
    }.get(name)
