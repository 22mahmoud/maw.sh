from django.forms import ValidationError
from wagtail import blocks
from wagtail.documents.blocks import DocumentChooserBlock

from src.base.constants import SOCIAL_PLATFORMS


class LinkStructValue(blocks.StructValue):
    def url(self):
        if self.get("internal_link"):
            return self["internal_link"].url

        if self.get("download_link"):
            return self["download_link"].url

        return self.get("external_link")


class LinkBlock(blocks.StructBlock):
    text = blocks.CharBlock(required=False, label="Link Text")

    prefix_icon = blocks.CharBlock(required=False, label="Prefix Icon")
    suffix_icon = blocks.CharBlock(required=False, label="Suffix Icon")
    icon = blocks.CharBlock(
        required=False,
        label="Icon-Only",
        help_text="For an icon-only link. Overrides prefix/suffix icons.",
    )

    size = blocks.ChoiceBlock(
        choices=[("sm", "Small"), ("md", "Medium"), ("lg", "Large")],
        default="md",
    )

    external_link = blocks.URLBlock(required=False)
    internal_link = blocks.PageChooserBlock(required=False)
    download_link = DocumentChooserBlock(required=False)

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
