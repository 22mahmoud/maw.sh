from django.http import HttpResponsePermanentRedirect
from django.utils.timezone import now


class SinglePostMixin:
    """Mixin for individual post functionality"""

    AUTO_GENERATE_TITLE = True
    URL_DATE_FORMAT = "%Y/%m/%d"
    TIMESTAMP_FORMAT = "%H%M%S"

    template = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.AUTO_GENERATE_TITLE and not self.pk:  # type: ignore
            self._auto_generate_title_and_slug()

    def _auto_generate_title_and_slug(self) -> None:
        timestamp = now().strftime(self.TIMESTAMP_FORMAT)
        self.title = self.generate_title(timestamp)  # type: ignore
        self.slug = self.generate_slug(timestamp)  # type: ignore

    @property
    def next_sibling(self):
        next_page = self.get_next_siblings().live().first()  # type: ignore
        return next_page.specific if next_page else None

    @property
    def prev_sibling(self):
        prev_page = self.get_prev_siblings().live().first()  # type: ignore
        return prev_page.specific if prev_page else None

    def generate_title(self, timestamp: str) -> str:
        return timestamp

    def generate_slug(self, timestamp: str) -> str:
        return timestamp

    def get_authors(self) -> list:
        if not hasattr(self, "page_person_relationship"):
            return []

        return [
            relationship.person
            for relationship in self.page_person_relationship.filter(  # type: ignore
                person__live=True
            ).select_related("person")
        ]

    def authors(self) -> list:
        return self.get_authors()

    @property
    def get_tags(self) -> list:
        if not hasattr(self, "tags"):
            return []

        tags = list(self.tags.all())  # type: ignore

        for tag in tags:
            tag.url = f"/tags/{tag.slug}/"

        return tags

    def serve(self, request, *args, **kwargs):
        canonical_url = self.url  # type: ignore
        if request.path != canonical_url:
            return HttpResponsePermanentRedirect(canonical_url)

        return super().serve(request, *args, **kwargs)  # type: ignore

    def get_absolute_url(self, request=None):
        return self.get_full_url(request)  # type: ignore

    def get_url_parts(self, request=None):
        response = super().get_url_parts(request)  # type: ignore
        if response is None:
            return None

        site_id, root_url, _ = response
        post_path = self._get_post_path()

        if post_path is None:
            return None

        url_prefix = self.get_parent().get_url(request=request).rstrip("/")  # type: ignore
        return (site_id, root_url, f"{url_prefix}/{post_path}")

    def _get_post_path(self) -> str | None:
        if not self.first_published_at or not self.slug:  # type: ignore
            return None

        parent = self.get_parent()  # type: ignore
        if not parent:
            return None

        parent = parent.specific

        if hasattr(parent, "reverse_subpage"):
            return parent.reverse_subpage(
                "archive",
                args=[
                    self.first_published_at.strftime("%Y"),  # type: ignore
                    self.first_published_at.strftime("%m"),  # type: ignore
                    self.first_published_at.strftime("%d"),  # type: ignore
                    self.slug,
                ],
            )

        date_part = self.first_published_at.strftime(self.URL_DATE_FORMAT)  # type: ignore
        return f"{date_part}/{self.slug}/"
