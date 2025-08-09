from urllib.parse import urljoin

from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed as DjangoFeed


class Feed(DjangoFeed):
    def __call__(self, request, *args, **kwargs):
        self.request = request
        return super().__call__(request, *args, **kwargs)


class FeedMixin:
    def _absolute_url(self, relative_url: str) -> str:
        if self.request:  # type: ignore
            return self.request.build_absolute_uri(relative_url)  # type: ignore

        site = Site.objects.get_current()
        return urljoin(f"https://{site.domain}", relative_url)

    def _item_categories(self, item):
        return [
            {
                "term": tag.name,
                "scheme": self._absolute_url(tag.url),
                "label": tag.slug.replace("-", " ").title(),
            }
            for tag in item.get_tags
        ]

    def _item_authors(self, item):
        return [
            {
                "name": getattr(person, "full_name", str(person)),
                "uri": person.website or person.get_absolute_url(),
                "email": getattr(person, "email", None),
            }
            for person in item.authors()
        ]

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return item.get_absolute_url()

    def item_guid(self, item):
        return self.item_link(item)

    def item_pubdate(self, item):
        return item.first_published_at

    def item_updateddate(self, item):
        return getattr(item, "latest_revision_created_at", item.first_published_at)

    def item_extra_kwargs(self, item):
        return {
            "content": item.body.render_as_block({"is_feed": True}),
            "_categories": self._item_categories(item),
            "_authors": self._item_authors(item),
        }
