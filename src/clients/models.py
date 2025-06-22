from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.embeds.blocks import EmbedBlock
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from src.base.blocks import HeadingBlock


class ClientIndexPage(Page):
    subpage_types = ["clients.ClientPage"]


class ClientPage(Page):
    client_url = models.URLField("Client Website", blank=True)
    icon = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    short_description = models.TextField(
        "Short Description",
        max_length=200,
        blank=True,
        help_text="Brief description for project listings",
    )

    project_type = models.CharField(
        "Project Type",
        max_length=100,
        blank=True,
        help_text="e.g., E-commerce, Corporate Website, Web App",
    )

    role = models.CharField(
        "My Position/Role",
        max_length=100,
        blank=True,
        help_text="e.g., Full-Stack Developer, Frontend Developer, Lead Developer",
    )

    technologies = models.CharField(
        "Technologies Used",
        max_length=200,
        blank=True,
        help_text="e.g., Django, React, PostgreSQL (comma-separated)",
    )

    start_date = models.DateField("Start Date", null=True, blank=True)
    end_date = models.DateField("End Date", null=True, blank=True)

    is_featured = models.BooleanField(
        "Featured Project", default=False, help_text="Show this project prominently"
    )

    body = StreamField(
        [
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
            ("quote", blocks.BlockQuoteBlock()),
            ("heading", HeadingBlock()),
            ("embed", EmbedBlock()),
            ("gallery", blocks.ListBlock(ImageChooserBlock(), label="Image Gallery")),
            ("code", blocks.TextBlock(label="Code Snippet")),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("client_url"),
                FieldPanel("icon"),
                FieldPanel("short_description"),
            ],
            heading="Basic Information",
        ),
        MultiFieldPanel(
            [
                FieldPanel("project_type"),
                FieldPanel("role"),
                FieldPanel("technologies"),
                FieldPanel("is_featured"),
            ],
            heading="Project Details",
        ),
        MultiFieldPanel(
            [
                FieldPanel("start_date"),
                FieldPanel("end_date"),
            ],
            heading="Timeline",
        ),
        FieldPanel("body"),
    ]

    parent_page_types = ["clients.ClientIndexPage"]
    subpage_types = []
