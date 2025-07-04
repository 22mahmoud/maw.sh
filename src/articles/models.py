from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.fields import StreamField
from wagtail.models import Page

from src.base.models import PageTag
from src.posts import BasePostsIndexPage, SinglePostMixin, get_post_content_panels
from src.posts.blocks import ArticleBlock
from src.seo.models import SeoMetaFields


class ArticlesPageIndex(BasePostsIndexPage):
    subpage_types = ["ArticlePage"]
    template = "archive/archive_page.html"

    def get_posts_queryset(self):
        return (
            ArticlePage.objects.child_of(self)  # type: ignore
            .live()
            .public()
            .order_by("-first_published_at")
        )


class ArticlePage(SinglePostMixin, SeoMetaFields, Page):  # type: ignore
    template = "archive/post_page.html"
    body = StreamField(
        [("article", ArticleBlock())],
        blank=False,
        use_json_field=True,
        min_num=1,
        max_num=1,
    )
    tags = ClusterTaggableManager(through=PageTag, blank=True)
    parent_page_types = ["ArticlesPageIndex"]
    subpage_types = []
    content_panels = get_post_content_panels()
