from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, MultipleChooserPanel
from wagtail.embeds.blocks import EmbedBlock
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Orderable, Page, ParentalKey
from wagtailmedia.blocks import VideoChooserBlock

from src.base.blocks.codeblock import CodeBlock
from src.base.blocks.list import ListBlock
from src.base.blocks.text import HeadingBlock


class ProjectPageTechnologyRelationship(Orderable):
    page = ParentalKey(
        "projects.ProjectPage",
        related_name="technology_relationships",
        on_delete=models.CASCADE,
    )

    technology = models.ForeignKey(
        "base.Technology",
        related_name="+",
        on_delete=models.CASCADE,
    )

    panels = [FieldPanel("technology")]


class ProjectsIndexPage(Page):
    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        projects = (
            ProjectPage.objects.child_of(self)  # type: ignore
            .live()
            .public()
            .order_by("-first_published_at")
        )

        context["projects"] = projects

        return context

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

    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    project_type = models.CharField("Project Type", max_length=100, blank=True)
    role = models.CharField("My Role", max_length=100, blank=True)

    start_date = models.DateField("Start Date", null=True, blank=True)
    end_date = models.DateField("End Date", null=True, blank=True)
    is_featured = models.BooleanField("Featured Project", default=False)

    @property
    def technologies(self):
        return [rel.technology for rel in self.technology_relationships.all()]  # type: ignore

    body = StreamField(
        [
            (
                "rich_text",
                blocks.RichTextBlock(
                    features=["bold", "italic", "link", "code", "blockquote"],
                    help_text="Write your article content. Use headings (H2, H3) to structure your text",
                ),
            ),
            (
                "image",
                ImageChooserBlock(
                    help_text="Choose an image from your media library to display alongside content"
                ),
            ),
            ("quote", blocks.BlockQuoteBlock()),
            ("gallery", blocks.ListBlock(ImageChooserBlock(), label="Image Gallery")),
            ("list", ListBlock()),
            ("codeblock", CodeBlock()),
            ("video", VideoChooserBlock()),
            ("embed", EmbedBlock()),
            ("heading", HeadingBlock()),
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
                FieldPanel("featured_image"),
                FieldPanel("role"),
                MultipleChooserPanel(
                    "technology_relationships",
                    chooser_field_name="technology",
                    heading="Technologies",
                    label="Technology",
                    panels=None,
                    min_num=0,
                ),
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
