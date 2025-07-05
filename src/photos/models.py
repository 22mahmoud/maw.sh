from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.fields import StreamField
from wagtail.models import Page

from src.base.models import PageTag
from src.posts import (
    BasePostsIndexPage,
    SinglePostMixin,
    get_post_content_panels,
    BasePostPage,
)
from src.posts.blocks import PhotoBlock
from src.seo.models import SeoMetaFields


class PhotosPageIndex(BasePostsIndexPage):
    subpage_types = ["PhotoPage"]
    template = "archive/archive_page.html"

    def get_posts_queryset(self):
        return (
            PhotoPage.objects.child_of(self)  # type: ignore
            .live()
            .public()
            .order_by("-first_published_at")
        )


class PhotoPage(BasePostPage, SinglePostMixin, SeoMetaFields, Page):  # type: ignore
    template = "archive/post_page.html"
    body = StreamField(
        [("photo", PhotoBlock())],
        use_json_field=True,
        blank=False,
        min_num=1,
        max_num=1,
    )
    tags = ClusterTaggableManager(through=PageTag, blank=True)
    parent_page_types = ["PhotosPageIndex"]
    subpage_types = []
    content_panels = get_post_content_panels()
