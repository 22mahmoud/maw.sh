from django.contrib.contenttypes.models import ContentType
from django.db.models import Prefetch
from django.db.models.fields.json import KeyTextTransform
from wagtail import blocks
from wagtail.models import Page

from src.posts.models import BasePostPage
from src.utils.get_subclasses import get_all_subclasses


class FeaturedBlogBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    posts = blocks.ListBlock(blocks.PageChooserBlock(page_type="articles.ArticlePage"))

    def get_context(self, value, parent_context=None):
        from src.articles.models import ArticlePage
        from src.base.models import PostPersonRelationship

        context = super().get_context(value, parent_context=parent_context)

        post_ids = [post.id for post in value["posts"] if post]

        posts_queryset = (
            ArticlePage.objects.filter(id__in=post_ids)
            .annotate(summary=KeyTextTransform("summary", "body__0__value"))
            .prefetch_related("tags")
            .prefetch_related(
                Prefetch(
                    "page_person_relationship",
                    queryset=PostPersonRelationship.objects.select_related("person__image"),
                )
            )
            .specific()  # type: ignore
        )

        ordered_posts = sorted(posts_queryset, key=lambda p: post_ids.index(p.id))  # type: ignore

        context["heading"] = value.get("heading")
        context["posts"] = ordered_posts
        return context

    class Meta:  # type: ignore
        template = "blocks/featured_blogs_block.html"
        icon = "star"
        label = "Featured Blog Post"


class FeedBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    limit = blocks.IntegerBlock(default=5, help_text="Number of recent posts to show")

    def get_context(self, value, parent_context=None):
        from src.articles.models import ArticlePage
        from src.base.models import PostPersonRelationship

        context = super().get_context(value, parent_context=parent_context)

        all_subclasses = get_all_subclasses(BasePostPage)
        all_content_types = ContentType.objects.get_for_models(*all_subclasses).values()
        excluded_content_type = ContentType.objects.get_for_model(ArticlePage)
        content_types = [ct for ct in all_content_types if ct.id != excluded_content_type.id]

        recent_posts = (
            Page.objects.live()  # type: ignore
            .public()
            .filter(content_type__in=content_types)
            .prefetch_related("tags")
            .prefetch_related(
                Prefetch(
                    "page_person_relationship",
                    queryset=PostPersonRelationship.objects.select_related("person__image"),
                ),
            )
            .specific()
            .order_by("-first_published_at")[: value["limit"]]
        )

        context["posts"] = [p.specific for p in recent_posts]

        return context

    class Meta:  # type: ignore
        template = "blocks/feed_block.html"
        icon = "list-ul"
        label = "Recent Posts Feed"
