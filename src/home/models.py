from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.http import Http404
from taggit.models import Tag
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, re_path
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtailmedia.blocks import VideoChooserBlock

from src.articles.models import ArticlePage
from src.base.blocks.button import ButtonBlock
from src.base.blocks.feed import FeaturedBlogBlock, FeedBlock
from src.base.blocks.hero import HeroBlock
from src.base.blocks.layout import FlexLayoutBlock, SpacerBlock
from src.base.blocks.link import SocialLinkStreamBlock
from src.base.models import Person
from src.clients.blocks import ClientsMarqueeStaticBlock
from src.pagination.mixins import PaginatedArchiveMixin
from src.posts.models import BasePostPage
from src.seo.models import SeoMetaFields
from src.utils import get_all_subclasses


class HomePage(PaginatedArchiveMixin, RoutablePageMixin, SeoMetaFields, Page):  # type: ignore
    introduction = models.TextField(help_text="Text to describe the page", blank=True)
    template = "base/generic_page.html"
    body = StreamField(
        [
            ("hero", HeroBlock()),
            ("clients", ClientsMarqueeStaticBlock()),
            ("social_links", SocialLinkStreamBlock()),
            ("Video", VideoChooserBlock()),
            ("button", ButtonBlock()),
            ("flex_layout", FlexLayoutBlock()),
            ("featured_blog", FeaturedBlogBlock()),
            ("feed", FeedBlock()),
            ("spacer", SpacerBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("body"),
    ]

    @re_path(r"^feed/(?:page/(?P<page>\d+)/?)?$", name="all_posts")
    def all_posts(self, request, page=1):
        """Posts by specific author with pagination"""

        all_post_types = self._get_filtered_posts({})
        article_page_content_type = ContentType.objects.get_for_model(ArticlePage)
        posts = all_post_types.exclude(content_type=article_page_content_type)

        return self._render_archive_page(
            request=request,
            posts=posts,
            page_number=page,
            base_url="/feed",
            title="Feed",
            introduction="this is an introduction",
        )

    @re_path(
        r"^authors/(?P<author_slug>[\w-]+)(/page/(?P<page>\d+))?/$",
        name="posts_by_author",
    )
    def posts_by_author(self, request, author_slug, page=1):
        """Posts by specific author with pagination"""
        try:
            author = Person.objects.get(slug=author_slug)
        except Person.DoesNotExist:
            raise Http404("Author not found")

        posts = self._get_filtered_posts({"page_person_relationship__person": author})

        return self._render_archive_page(
            request=request,
            posts=posts,
            page_number=page,
            base_url=f"/authors/{author_slug}",
            title=f'Posts By "{author.full_name}"',
            introduction="this is an introduction",
            extra_context={"author": author},
        )

    @re_path(r"^tags/(?P<tag_slug>[\w-]+)(/page/(?P<page>\d+))?/$", name="posts_by_tag")
    def posts_by_tag(self, request, tag_slug, page=1):
        """Posts by specific tag with pagination"""
        try:
            tag = Tag.objects.get(slug=tag_slug)
        except Tag.DoesNotExist:
            raise Http404("Tag not found")

        posts = self._get_filtered_posts({"tagged_items__tag__slug": tag_slug})

        return self._render_archive_page(
            request=request,
            posts=posts,
            page_number=page,
            base_url=f"/tags/{tag_slug}",
            title=f'Posts tagged "#{tag.name}"',
            introduction="this is an introduction",
            extra_context={"tag": tag},
        )

    def _get_filtered_posts(self, filter_kwargs, order_by="-first_published_at"):
        """Get filtered and ordered posts"""

        all_subclasses = get_all_subclasses(BasePostPage)

        content_types = ContentType.objects.get_for_models(*all_subclasses).values()

        return (
            Page.objects.live()  # type: ignore
            .public()
            .filter(content_type__in=content_types)
            .filter(**filter_kwargs)
            .order_by(order_by)
        )

    def _render_archive_page(
        self,
        request,
        posts,
        page_number,
        base_url,
        title,
        introduction,
        extra_context=None,
    ):
        if not posts.exists():
            raise Http404("No posts found")

        paginated_posts = self.paginate_posts(posts, page_number, base_url)
        paginated_posts.object_list = [p.specific for p in paginated_posts.object_list]  # type: ignore

        context = self.get_paginated_context(request, paginated_posts=paginated_posts)
        context["page"].title = title
        context["page"].introduction = introduction

        if extra_context:
            context.update(extra_context)

        return self.render(
            request,
            context_overrides=context,
            template="archive/archive_page.html",
        )
