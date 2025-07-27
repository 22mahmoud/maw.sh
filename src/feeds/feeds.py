# pyright: reportAttributeAccessIssue=false
from itertools import chain

from django.utils.html import escape, strip_tags
from django.utils.safestring import mark_safe

from src.articles.models import ArticlePage
from src.posts.models import BasePostPage
from src.utils.get_subclasses import get_all_subclasses

from .generators import ExtendedAtomFeed
from .mixins import Feed, FeedMixin


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
        posts = chain.from_iterable(cls.objects.live().specific() for cls in subclasses)
        return sorted(posts, key=lambda p: p.first_published_at, reverse=True)[:100]

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


class LatestBlogsFeed(FeedMixin, Feed):
    feed_type = ExtendedAtomFeed
    title = "Mahmoud Ashraf – Blog Articles"
    link = "/blog/"
    subtitle = (
        "Long-form writing by Mahmoud Ashraf, "
        "a front-end developer sharing insights from Alexandria, Egypt."
    )

    def items(self):
        return ArticlePage.objects.live().specific().order_by("-first_published_at")[:100]

    def item_description(self, item):
        if not item.body or not item.body.stream_data:
            return ""

        try:
            block = item.body[0]
        except IndexError:
            return ""

        return mark_safe(block.value.get("summary", ""))
