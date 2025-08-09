from django.http import HttpResponsePermanentRedirect
from django.utils.timezone import now
from wagtail import blocks

from src.posts.utils import extract_headings_from_streamblock


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
    def seo_author(self) -> str:
        authors = self.get_authors()
        if authors:
            names = [a.full_name for a in authors if a]
            return ", ".join(filter(None, names))

        return ""

    @property
    def next_sibling(self):
        return self.get_next_siblings().live().first()  # type: ignore

    @property
    def prev_sibling(self):
        return self.get_prev_siblings().live().first()  # type: ignore

    @property
    def toc(self):
        if not self.body:  # type: ignore
            return []

        items = []
        for block in self.body:  # type: ignore
            body = block.value.get("body")
            if isinstance(body, blocks.StreamValue):
                items.extend(extract_headings_from_streamblock(body))

        return items

    def generate_title(self, timestamp: str) -> str:
        return timestamp

    def generate_slug(self, timestamp: str) -> str:
        return timestamp

    def get_authors(self) -> list:
        # If not prefetched, this will still hit the DB lazily.
        relationships = getattr(self, "page_person_relationship", None)
        if relationships is None:
            return []

        return [rel.person for rel in relationships.all() if rel.person.live]

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

        site_id, root_url, page_path = response
        if not self.first_published_at or not self.slug:  # type: ignore
            return None

        try:
            url_prefix, _ = page_path.rsplit(self.slug + "/", 1)
        except ValueError:
            return response

        date_part = self.first_published_at.strftime(self.URL_DATE_FORMAT)  # type: ignore
        new_page_path = f"{url_prefix}{date_part}/{self.slug}/"

        return (site_id, root_url, new_page_path)
