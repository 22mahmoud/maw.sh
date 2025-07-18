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

    return panels


def get_post_search_fields():
    search_fields = Page.search_fields.copy()
    search_fields.append(index.SearchField("body"))
    search_fields.append(index.SearchField("tags"))
    return search_fields
