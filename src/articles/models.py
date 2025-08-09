from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.fields import StreamField

from src.base.models import PageTag
from src.posts.blocks import ArticleBlock
from src.posts.models import BasePostPage, BasePostsIndexPage
from src.posts.utils import get_post_content_panels, get_post_search_fields


class ArticlesPageIndex(BasePostsIndexPage):
    POSTS_PER_PAGE = 10000
    subpage_types = ["ArticlePage"]
    template = "archive/blog_page.html"

    def get_posts_queryset(self):
        return (
            ArticlePage.objects.child_of(self)  # type: ignore
            .live()
            .public()
            .order_by("-first_published_at")
        )


class ArticlePage(BasePostPage):  # type: ignore
    template = "archive/post_page.html"
    body = StreamField(
        [("article", ArticleBlock())],
        blank=False,
        use_json_field=True,
        min_num=1,
        max_num=1,
    )
    tags = ClusterTaggableManager(through=PageTag, blank=True)

    seo_description_sources = ["search_description", ["body", 0, "summary"]]

    parent_page_types = ["ArticlesPageIndex"]
    subpage_types = []
    content_panels = get_post_content_panels()
    search_fields = get_post_search_fields()
