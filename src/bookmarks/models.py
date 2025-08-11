from wagtail.fields import StreamField

from src.posts.blocks import BookmarkBlock
from src.posts.models import BasePostPage, BasePostsIndexPage
from src.posts.utils import get_post_content_panels, get_post_search_fields


class BookmarksPageIndex(BasePostsIndexPage):
    subpage_types = ["BookmarkPage"]
    template = "archive/archive_page.html"

    def get_posts_queryset(self):
        return (
            BookmarkPage.objects.child_of(self)  # type: ignore
            .live()
            .public()
            .order_by("-first_published_at")
        )


class BookmarkPage(BasePostPage):  # type: ignore
    template = "archive/post_page.html"
    body = StreamField(
        [("bookmark", BookmarkBlock())],
        blank=False,
        min_num=1,
        max_num=1,
        use_json_field=True,
    )
    parent_page_types = ["BookmarksPageIndex"]
    subpage_types = []
    content_panels = get_post_content_panels()
    search_fields = get_post_search_fields()
