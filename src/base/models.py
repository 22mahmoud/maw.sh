from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from modelcluster.models import ClusterableModel
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel, ObjectList, TabbedInterface
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import StreamField
from wagtail.models import (
    DraftStateMixin,
    LockableMixin,
    Orderable,
    Page,
    ParentalKey,
    RevisionMixin,
    WorkflowMixin,
)
from wagtail.models.pages import slugify
from wagtailmedia.blocks import VideoChooserBlock

from src.clients.blocks import ClientsMarqueeStaticBlock
from src.seo.models import SeoMetaFields

from .blocks import ButtonBlock, HeroBlock, SocialLinkStreamBlock
from .constants import SOCIAL_PLATFORMS


class PageTag(TaggedItemBase):
    content_object = ParentalKey(
        "wagtailcore.Page",
        related_name="tagged_items",
        on_delete=models.CASCADE,
    )


class PostPersonRelationship(Orderable, models.Model):
    page = ParentalKey(
        "wagtailcore.Page",
        related_name="page_person_relationship",
        on_delete=models.CASCADE,
    )

    person = models.ForeignKey(
        "base.Person",
        related_name="person_page_relationship",
        on_delete=models.CASCADE,
    )

    panels = [FieldPanel("person")]


class Technology(models.Model):
    name = models.CharField(max_length=50, unique=True)
    icon = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    @property
    def thumb_icon(self):
        try:
            return self.icon.get_rendition("fill-50x50").img_tag()  # type: ignore
        except:  # noqa: E722
            return ""

    def __str__(self):
        return self.name


class Person(  # type: ignore
    WorkflowMixin,
    DraftStateMixin,
    LockableMixin,
    RevisionMixin,
    ClusterableModel,
):
    class Meta:  # type: ignore
        verbose_name = "person"
        verbose_name_plural = "people"

    first_name = models.CharField("First name", max_length=254)
    last_name = models.CharField("Last name", max_length=254)
    title = models.CharField("Title", blank=True, max_length=254)
    bio = models.TextField("Bio", blank=True, max_length=254)

    slug = models.SlugField(
        null=True,
        max_length=255,
        unique=True,
        blank=True,
        editable=True,
    )

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    workflow_states = GenericRelation(  # type: ignore
        "wagtailcore.WorkflowState",
        content_type_field="base_content_type",
        object_id_field="object_id",
        related_query_name="person",
        for_concrete_model=False,
    )

    _revisions = GenericRelation(
        "wagtailcore.Revision",
        content_type_field="base_content_type",
        object_id_field="object_id",
        related_query_name="person",
        for_concrete_model=False,
    )

    @property
    def revisions(self):
        return self._revisions

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def thumb_image(self):
        try:
            return self.image.get_rendition("fill-50x50").img_tag()  # type: ignore
        except:  # noqa: E722
            return ""

    def clean(self):
        super().clean()

        if not self.slug:
            self.slug = slugify(f"{self.first_name} {self.last_name}")

        qs = Person.objects.filter(slug=self.slug)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError({"slug": "A person with this slug already exists."})

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class GenericPage(SeoMetaFields, Page):  # type: ignore
    introduction = models.TextField(help_text="Text to describe the page", blank=True)

    body = StreamField(
        [
            ("hero", HeroBlock()),
            ("clients", ClientsMarqueeStaticBlock()),
            ("social_links", SocialLinkStreamBlock()),
            ("Video", VideoChooserBlock()),
            ("button", ButtonBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("body"),
    ]


@register_setting(icon="site")
class SiteSettings(BaseSiteSetting):
    avilable_for_projects = models.BooleanField(
        verbose_name=_("Avilable for projects"), default=False
    )

    twitter = models.CharField(
        blank=True,
        verbose_name=_("Twitter"),
    )

    mastodon = models.CharField(
        blank=True,
        verbose_name=_("Mastodon"),
    )

    youtube = models.CharField(
        blank=True,
        verbose_name=_("Youtube"),
    )

    reddit = models.CharField(
        blank=True,
        verbose_name=_("Reddit"),
    )

    github = models.CharField(
        blank=True,
        verbose_name=_("Github"),
    )

    pixelfed = models.CharField(
        blank=True,
        verbose_name=_("Pixelfed.social"),
    )

    linkedin = models.CharField(
        blank=True,
        verbose_name=_("Linkedin"),
    )

    bluesky = models.CharField(
        blank=True,
        verbose_name=_("Bluesky"),
    )

    @cached_property
    def social_links(self):
        return [
            {
                "text": SOCIAL_PLATFORMS[key]["label"],
                "url": SOCIAL_PLATFORMS[key]["url_pattern"].format(getattr(self, key)),
                "icon": SOCIAL_PLATFORMS[key]["icon"],
                "platform": key,
            }
            for key in SOCIAL_PLATFORMS
            if getattr(self, key)
        ]

    edit_handler = TabbedInterface(
        [
            ObjectList(
                [
                    FieldPanel("avilable_for_projects"),
                ],
                heading="General",
            ),
            ObjectList(
                [
                    FieldPanel("twitter"),
                    FieldPanel("mastodon"),
                    FieldPanel("bluesky"),
                    FieldPanel("pixelfed"),
                    FieldPanel("youtube"),
                    FieldPanel("reddit"),
                    FieldPanel("github"),
                    FieldPanel("linkedin"),
                ],
                heading="Social Media",
            ),
        ]
    )
