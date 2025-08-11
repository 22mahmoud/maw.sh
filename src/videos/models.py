from wagtail.fields import StreamField

from src.posts.blocks import VideoBlock
from src.posts.models import BasePostPage, BasePostsIndexPage
from src.posts.utils import get_post_content_panels, get_post_search_fields


class VideosPageIndex(BasePostsIndexPage):
    subpage_types = ["VideoPage"]
    template = "archive/archive_page.html"

    def get_posts_queryset(self):
        return (
            VideoPage.objects.child_of(self)  # type: ignore
            .live()
            .public()
            .order_by("-first_published_at")
        )


class VideoPage(BasePostPage):  # type: ignore
    template = "archive/post_page.html"
    body = StreamField(
        [("video", VideoBlock())],
        use_json_field=True,
        blank=False,
        min_num=1,
        max_num=1,
    )
    parent_page_types = ["VideosPageIndex"]
    subpage_types = []
    content_panels = get_post_content_panels()
    search_fields = get_post_search_fields()
