from collections import OrderedDict

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, re_path
from wagtail.models import Page

from src.pagination import PaginatedArchiveMixin
from src.posts.mixins import SinglePostMixin
from src.seo.models import SeoMetaFields
from src.webmentions.models import (
    BookmarkWebmention,
    LikeWebmention,
    MentionWebmention,
    ReplyWebmention,
    RepostWebmention,
    Webmention,
)


class BasePostPage(SinglePostMixin, SeoMetaFields):  # type: ignore
    legacy_url_path = models.CharField(
        max_length=512,
        blank=True,
        null=True,
        unique=True,
        db_index=True,
        help_text="The full path of the URL from the old static site (e.g., /blog/old-slug).",
    )

    @property
    def webmentions(self):
        groups = OrderedDict(
            [
                ("likes", []),
                ("reposts", []),
                ("bookmarks", []),
                ("replies", []),
                ("mentions", []),
            ]
        )

        mentions = self._get_webmentions()

        for mention in mentions:
            if isinstance(mention, LikeWebmention):
                groups["likes"].append(mention)
            elif isinstance(mention, RepostWebmention):
                groups["reposts"].append(mention)
            elif isinstance(mention, BookmarkWebmention):
                groups["bookmarks"].append(mention)
            elif isinstance(mention, ReplyWebmention):
                groups["replies"].append(mention)
            elif isinstance(mention, MentionWebmention):
                groups["mentions"].append(mention)

        return {
            name: mentions_list
            for name, mentions_list in groups.items()
            if mentions_list
        }

    def _get_webmentions(self):
        current_url = self.get_full_url()
        query = Q(wm_target=current_url)

        if self.legacy_url_path:
            if hasattr(settings, "LEGACY_SITE_DOMAIN"):
                legacy_domain = settings.LEGACY_SITE_DOMAIN
                legacy_url_https = f"https://{legacy_domain}{self.legacy_url_path}"
                legacy_url_http = f"http://{legacy_domain}{self.legacy_url_path}"
                query |= Q(wm_target=legacy_url_https) | Q(wm_target=legacy_url_http)
            query |= Q(wm_target__endswith=self.legacy_url_path)

        return (
            Webmention.objects.filter(query)
            .select_related("author")
            .order_by("wm_received")
        )

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
