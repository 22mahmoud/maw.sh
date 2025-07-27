# pyright: reportAttributeAccessIssue=false
from django.contrib.syndication.views import Feed
from django.utils import feedgenerator
from django.utils.html import escape, strip_tags

from src.articles.models import ArticlePage
from src.posts.models import BasePostPage
from src.utils.get_subclasses import get_all_subclasses

from .mixins import FeedMixin


class ExtendedAtomFeed(feedgenerator.Atom1Feed):
    def add_item_elements(self, handler, item):
        super().add_item_elements(handler, item)

        for cat in item.get("_categories", []):
            attrs = {"term": cat["term"]}
            if "scheme" in cat:
                attrs["scheme"] = cat["scheme"]
            if "label" in cat:
                attrs["label"] = cat["label"]
            handler.addQuickElement("category", None, attrs)

        content = item.get("content")
        if content:
            handler.addQuickElement("content", content, {"type": "html"})


class LatestFeed(FeedMixin, Feed):
    feed_type = ExtendedAtomFeed
    title = "Mahmoud Ashraf – Latest Social Posts"
    link = "/feed/"
    subtitle = "Short-form posts, replies, likes, and other micro-updates by Mahmoud Ashraf."
    author_name = "Mahmoud Ashraf"

    def _get_subclasses(self):
        all_subclasses = get_all_subclasses(BasePostPage)
        return [cls for cls in all_subclasses if cls != ArticlePage]

    def items(self):
        subclasses = self._get_subclasses()
        items = []
        for subclass in subclasses:
            items += list(subclass.objects.live().specific())
        return sorted(items, key=lambda p: p.first_published_at, reverse=True)[:10]

    def item_description(self, item):
        if not item.body or not item.body[0]:
            return ""

        block = item.body[0]
        value = block.value
        block_type = block.block_type

        def url_summary(action, url):
            return f"{action} <a href='{escape(url)}'>{escape(url)}</a>" if url else ""

        match block_type:
            case "note":
                return strip_tags(value.get("content", ""))

            case "reply":
                return url_summary("Replied to", value.get("in_reply_to"))

            case "like":
                return url_summary("Liked", value.get("like_of"))

            case "bookmark":
                return url_summary("Bookmarked", value.get("bookmark_of"))

            case "repost":
                return url_summary("Reposted", value.get("repost_of"))

            case "photo":
                caption = value.get("caption")
                return strip_tags(caption) if caption else "Shared a photo"

            case "video":
                caption = value.get("caption")
                return strip_tags(caption) if caption else "Shared a video"

            case "article":
                return strip_tags(value.get("summary", ""))

            case _:
                return ""


class LatestBLogsFeed(FeedMixin, Feed):
    feed_type = ExtendedAtomFeed
    title = "Mahmoud Ashraf – Blog Articles"
    subtitle = (
        "Long-form writing by Mahmoud Ashraf, "
        "a front-end developer sharing insights from Alexandria, Egypt."
    )
    link = "/blog/"
    subtitle = "Mahmoud Ashraf is a Front-end developer based in Alexandria, Egypt."

    def items(self):
        return ArticlePage.objects.live().specific().order_by("-first_published_at")[:10]

    def item_description(self, item):
        block = item.body[0]
        if block.block_type == "article":
            return block.value.get("summary", "")
        return ""
