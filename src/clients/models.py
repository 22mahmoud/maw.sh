from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from wagtail.models import DraftStateMixin, LockableMixin, RevisionMixin, WorkflowMixin


class Client(  # type: ignore
    WorkflowMixin, DraftStateMixin, LockableMixin, RevisionMixin, models.Model
):
    name = models.CharField(max_length=255)
    website = models.URLField(blank=True)
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    featured = models.BooleanField(default=False, help_text="Show in homepage marquee")
    _revisions = GenericRelation("wagtailcore.Revision", related_query_name="client")
    workflow_states = GenericRelation(  # type: ignore
        "wagtailcore.WorkflowState",
        content_type_field="base_content_type",
        object_id_field="object_id",
        related_query_name="advert",
        for_concrete_model=False,
    )

    @property
    def revisions(self):
        return self._revisions

    def __str__(self):
        return self.name
