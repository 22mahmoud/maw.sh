from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField


class HomePage(Page):
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Hero Profile Picture",
    )

    hero_headline = models.CharField(max_length=255, help_text="Write A Hero Headline")

    hero_text = RichTextField(help_text="Write A Hero body text")

    hero_cta = models.CharField(
        verbose_name="Hero CTA",
        max_length=255,
        help_text="Text to display on Call to Action",
        default="Contact",
    )

    hero_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Hero CTA link",
        help_text="Choose a page to link to for the Call to Action",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_image"),
                FieldPanel("hero_headline"),
                FieldPanel("hero_text"),
                MultiFieldPanel(
                    [
                        FieldPanel("hero_cta"),
                        FieldPanel("hero_cta_link"),
                    ],
                ),
            ],
            heading="Hero section",
        ),
    ]
