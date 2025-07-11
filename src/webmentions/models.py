from django.db import models
from django.utils.dateparse import parse_datetime
from polymorphic.models import PolymorphicModel
from wagtail.fields import RichTextField


class WebmentionAuthor(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    photo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    @property
    def photo_preview(self):
        try:
            return self.photo.get_rendition("fill-100x100").img_tag()  # type: ignore
        except Exception:
            return ""

    def __str__(self):  # type: ignore
        return self.name or self.url


class Webmention(PolymorphicModel):
    _model_registry: dict[str, type["Webmention"]] = {}
    _wm_property: str | None = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls._wm_property:
            if cls._wm_property in cls._model_registry:
                raise TypeError(f"Duplicate wm_property '{cls._wm_property}' found.")
            cls._model_registry[cls._wm_property] = cls

    @classmethod
    def create_from_api_data(
        cls, mention_data: dict, author: "WebmentionAuthor"
    ) -> "Webmention":
        """
        Factory method: Creates the correct Webmention subclass from raw API data.
        """
        wm_property = mention_data.get("wm-property")

        ModelClass = cls._model_registry.get(wm_property, Webmention)  # type: ignore

        instance_data = {
            "author": author,
            "wm_id": mention_data.get("wm-id"),
            "wm_source": mention_data.get("wm-source"),
            "wm_target": mention_data.get("wm-target"),
            "wm_protocol": mention_data.get("wm-protocol"),
            "wm_property": wm_property,
            "wm_private": mention_data.get("wm-private", False),
            "url": mention_data.get("url"),
        }

        if published_str := mention_data.get("published"):
            instance_data["published"] = parse_datetime(published_str)

        if received_str := mention_data.get("wm-received"):
            instance_data["wm_received"] = parse_datetime(received_str)

        specific_data = ModelClass._extract_specific_data(mention_data)
        instance_data.update(specific_data)

        return ModelClass(**instance_data)

    @classmethod
    def _extract_specific_data(cls, mention_data: dict) -> dict:
        """Hook for subclasses to extract their own unique fields."""
        return {}

    wm_id = models.BigIntegerField(unique=True)
    wm_source = models.URLField(max_length=1024)
    wm_target = models.URLField(max_length=1024)
    wm_protocol = models.CharField(max_length=50)
    wm_received = models.DateTimeField()
    wm_property = models.CharField(max_length=50)
    wm_private = models.BooleanField(default=False)

    url = models.URLField(max_length=1024, blank=True, null=True)
    published = models.DateTimeField(blank=True, null=True)

    author = models.ForeignKey(
        WebmentionAuthor,
        on_delete=models.SET_NULL,
        null=True,
        related_name="webmentions",
    )

    @property
    def get_type(self):
        return self.get_real_instance_class().__name__.replace("Webmention", "")  # type: ignore

    def __str__(self):
        return f"{self.get_type}: {self.author} → {self.wm_target}"


class LikeWebmention(Webmention):
    _wm_property = "like-of"
    like_of = models.URLField(max_length=1024)

    @classmethod
    def _extract_specific_data(cls, mention_data: dict) -> dict:
        return {"like_of": mention_data.get("like-of")}


class ReplyWebmention(Webmention):
    _wm_property = "in-reply-to"
    in_reply_to = models.URLField(max_length=1024)
    content_text = models.TextField(blank=True)
    content_html = RichTextField(blank=True)

    @classmethod
    def _extract_specific_data(cls, mention_data: dict) -> dict:
        content = mention_data.get("content", {})
        return {
            "in_reply_to": mention_data.get("in-reply-to"),
            "content_text": content.get("text", ""),
            "content_html": content.get("html", ""),
        }


class RepostWebmention(Webmention):
    _wm_property = "repost-of"
    repost_of = models.URLField(max_length=1024)

    @classmethod
    def _extract_specific_data(cls, mention_data: dict) -> dict:
        return {"repost_of": mention_data.get("repost-of")}


class BookmarkWebmention(Webmention):
    _wm_property = "bookmark-of"
    bookmark_of = models.URLField(max_length=1024)

    @classmethod
    def _extract_specific_data(cls, mention_data: dict) -> dict:
        return {"bookmark_of": mention_data.get("bookmark-of")}


class MentionWebmention(Webmention):
    _wm_property = "mention-of"
    mention_of = models.URLField(max_length=1024)

    @classmethod
    def _extract_specific_data(cls, mention_data: dict) -> dict:
        return {"mention_of": mention_data.get("mention-of")}


class RSVPWebmention(Webmention):
    _wm_property = "rsvp"
    rsvp = models.CharField(
        max_length=20,
        choices=[
            ("yes", "Yes"),
            ("no", "No"),
            ("maybe", "Maybe"),
            ("interested", "Interested"),
        ],
    )

    @classmethod
    def _extract_specific_data(cls, mention_data: dict) -> dict:
        return {"rsvp": mention_data.get("rsvp")}


class WebmentionSync(models.Model):
    last_sync = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Webmention Sync State"

    class Meta:
        verbose_name_plural = "Webmention Sync State"

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
