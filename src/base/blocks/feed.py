from django.contrib.contenttypes.models import ContentType
from wagtail import blocks
from wagtail.models import Page

from src.posts.models import BasePostPage
from src.utils.get_subclasses import get_all_subclasses


class FeaturedBlogBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    posts = blocks.ListBlock(blocks.PageChooserBlock(page_type="articles.ArticlePage"))

    class Meta:  # type: ignore
        template = "blocks/featured_blogs_block.html"
        icon = "star"
        label = "Featured Blog Post"


class FeedBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    limit = blocks.IntegerBlock(default=5, help_text="Number of recent posts to show")

    def get_context(self, value, parent_context=None):
        from src.articles.models import ArticlePage

        context = super().get_context(value, parent_context=parent_context)

        all_subclasses = get_all_subclasses(BasePostPage)
        all_content_types = ContentType.objects.get_for_models(*all_subclasses)
        excluded_content_types = ContentType.objects.get_for_model(ArticlePage)
        content_types = [ct for _, ct in all_content_types.items() if ct != excluded_content_types]

        recent_posts = (
            Page.objects.live()  # type: ignore
            .public()
            .filter(content_type__in=content_types)
            .order_by("-first_published_at")[: value["limit"]]
        )

        context["posts"] = [p.specific for p in recent_posts]

        return context

    class Meta:  # type: ignore
        template = "blocks/feed_block.html"
        icon = "list-ul"
        label = "Recent Posts Feed"
