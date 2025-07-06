from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.fields import StreamField
from wagtail.models import Page

from src.base.models import PageTag
from src.posts import (
    BasePostPage,
    BasePostsIndexPage,
    SinglePostMixin,
    get_post_content_panels,
)
from src.posts.blocks import VideoBlock
from src.seo.models import SeoMetaFields


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


class VideoPage(BasePostPage, SinglePostMixin, SeoMetaFields, Page):  # type: ignore
    template = "archive/post_page.html"
    body = StreamField(
        [("video", VideoBlock())],
        use_json_field=True,
        blank=False,
        min_num=1,
        max_num=1,
    )
    tags = ClusterTaggableManager(through=PageTag, blank=True)
    parent_page_types = ["VideosPageIndex"]
    subpage_types = []
    content_panels = get_post_content_panels()
