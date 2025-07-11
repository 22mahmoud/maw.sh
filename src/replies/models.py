from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.fields import StreamField

from src.base.models import PageTag
from src.posts.blocks import ReplyBlock
from src.posts.models import BasePostPage, BasePostsIndexPage
from src.posts.utils import get_post_content_panels


class RepliesPageIndex(BasePostsIndexPage):
    subpage_types = ["ReplyPage"]
    template = "archive/archive_page.html"

    def get_posts_queryset(self):
        return (
            ReplyPage.objects.child_of(self)  # type: ignore
            .live()
            .public()
            .order_by("-first_published_at")
        )


class ReplyPage(BasePostPage):  # type: ignore
    template = "archive/post_page.html"
    body = StreamField(
        [("reply", ReplyBlock())],
        blank=False,
        min_num=1,
        max_num=1,
        use_json_field=True,
    )
    tags = ClusterTaggableManager(through=PageTag, blank=True)
    parent_page_types = ["RepliesPageIndex"]
    subpage_types = []
    content_panels = get_post_content_panels()
