from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.embeds.blocks import EmbedBlock
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from src.base.blocks import HeadingBlock


class ProjectsIndexPage(Page):
    subpage_types = ["projects.ProjectPage"]


class ProjectPage(Page):
    client = models.ForeignKey(
        "clients.Client",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="projects",
    )

    short_description = models.TextField(
        "Short Description",
        max_length=200,
        blank=True,
    )

    project_type = models.CharField("Project Type", max_length=100, blank=True)
    role = models.CharField("My Role", max_length=100, blank=True)
    technologies = models.CharField("Technologies Used", max_length=200, blank=True)

    start_date = models.DateField("Start Date", null=True, blank=True)
    end_date = models.DateField("End Date", null=True, blank=True)
    is_featured = models.BooleanField("Featured Project", default=False)

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
        FieldPanel("client"),
        MultiFieldPanel(
            [
                FieldPanel("short_description"),
                FieldPanel("project_type"),
                FieldPanel("role"),
                FieldPanel("technologies"),
                FieldPanel("is_featured"),
            ],
            heading="Project Info",
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

    parent_page_types = ["projects.ProjectsIndexPage"]
    subpage_types = []
