from django.db import models
from django.http import Http404
from django.shortcuts import get_object_or_404
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, re_path
from wagtail.models import Page

from src.pagination import PaginatedArchiveMixin
from src.posts.mixins import SinglePostMixin
from src.seo.models import SeoMetaFields


class BasePostPage(SinglePostMixin, SeoMetaFields):  # type: ignore
    class Meta:  # type: ignore
        abstract = True


class BasePostsIndexPage(PaginatedArchiveMixin, SeoMetaFields, RoutablePageMixin, Page):
    """Base class for post index pages with pagination and routing"""

    introduction = models.TextField(help_text="Text to describe the page", blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
    ]

    class Meta:  # type: ignore
        abstract = True

    @re_path(r"^(\d{4})/(\d{2})/(\d{2})/(.+)/$", name="archive")
    def archive_by_date_slug(self, request, year, month, day, slug):
        """Route for individual archive: /yyyy/mm/dd/slug/"""
        try:
            year, month, day = int(year), int(month), int(day)
        except ValueError:
            raise Http404("Invalid date format")

        post = get_object_or_404(
            self.get_posts_queryset(),
            slug=slug,
            first_published_at__year=year,
            first_published_at__month=month,
            first_published_at__day=day,
        )

        return post.specific.serve(request)

    @re_path(r"^$")
    @re_path(r"^page/(?P<page>\d+)/$")
    def paginated_posts(self, request, page=1):
        """Main archive page with pagination"""
        posts = self.get_posts_queryset()
        paginated_posts = self.paginate_posts(posts, page_number=page)
        context = self.get_paginated_context(request, paginated_posts=paginated_posts)
        return self.render(request, context_overrides=context)
