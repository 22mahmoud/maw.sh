from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.fields import StreamField
from wagtail.models import Page

from src.base.models import PageTag
from src.posts import BasePostsIndexPage, SinglePostMixin, get_post_content_panels
from src.posts.blocks import ReplyBlock
from src.seo.models import SeoMetaFields


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


class ReplyPage(SinglePostMixin, SeoMetaFields, Page):  # type: ignore
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
