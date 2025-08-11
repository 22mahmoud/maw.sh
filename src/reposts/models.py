from wagtail.fields import StreamField

from src.posts.blocks import RepostBlock
from src.posts.models import BasePostPage, BasePostsIndexPage
from src.posts.utils import get_post_content_panels, get_post_search_fields


class RepostsPageIndex(BasePostsIndexPage):
    subpage_types = ["RepostPage"]
    template = "archive/archive_page.html"

    def get_posts_queryset(self):
        return (
            RepostPage.objects.child_of(self)  # type: ignore
            .live()
            .public()
            .order_by("-first_published_at")
        )


class RepostPage(BasePostPage):  # type: ignore
    template = "archive/post_page.html"
    body = StreamField(
        [("repost", RepostBlock())],
        use_json_field=True,
        blank=False,
        min_num=1,
        max_num=1,
    )
    parent_page_types = ["RepostsPageIndex"]
    subpage_types = []
    content_panels = get_post_content_panels()
    search_fields = get_post_search_fields()
