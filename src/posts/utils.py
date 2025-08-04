from django.utils.html import strip_tags
from django.utils.text import slugify
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, MultipleChooserPanel
from wagtail.models import Page
from wagtail.search import index


def get_post_content_panels(include_body=True, include_tags=True, include_authors=True):
    """Generate content panels for post pages"""
    panels = Page.content_panels.copy()

    if include_body:
        panels.append(FieldPanel("body"))  # type: ignore

    if include_tags:
        panels.append(FieldPanel("tags"))  # type: ignore

    if include_authors:
        panels.append(
            MultipleChooserPanel(  # type: ignore
                "page_person_relationship",
                chooser_field_name="person",
                heading="Authors",
                label="Author",
                panels=None,
                min_num=1,
            )
        )

    panels.append(
        MultiFieldPanel(  # type: ignore
            [
                FieldPanel("legacy_url_path"),
            ],
            heading="Legacy Migration",
        )
    )

    panels.append(FieldPanel("first_published_at"))  # type:ignore
    panels.append(FieldPanel("last_published_at", read_only=True))  # type:ignore

    return panels


def get_post_search_fields():
    search_fields = Page.search_fields.copy()
    search_fields.append(index.SearchField("body"))
    search_fields.append(index.SearchField("tags"))
    return search_fields


def extract_headings_from_streamblock(stream_data):
    toc = []

    for block in stream_data:
        block_type = block.block_type
        block_value = block.value

        if block_type == "heading" and block_value.get("use_anchor", False):
            heading_text = strip_tags(block_value.get("heading_text", ""))
            size = block_value.get("size", "h2")
            depth = int(size[1:]) if size.startswith("h") and size[1:].isdigit() else 2

            toc.append(
                {
                    "text": heading_text,
                    "slug": slugify(heading_text),
                    "size": size,
                    "depth": depth,
                }
            )

        elif isinstance(block_value, blocks.StreamValue):
            toc.extend(extract_headings_from_streamblock(block_value))

        elif isinstance(block_value, dict):
            for val in block_value.values():
                if isinstance(val, blocks.StreamValue):
                    toc.extend(extract_headings_from_streamblock(val))

    return toc
