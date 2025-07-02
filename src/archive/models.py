from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from wagtail.admin.panels import FieldPanel, MultipleChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, re_path
from wagtail.models import Orderable, Page, ParentalKey
from wagtail.models.pages import StreamField

from src.base.models import Person
from src.seo.models import SeoMetaFields

from .blocks import (
    ArticleBlock,
    BookmarkBlock,
    LikeBlock,
    NoteBlock,
    PhotoBlock,
    ReplyBlock,
    RepostBlock,
    VideoBlock,
)


class PostPersonRelationship(Orderable, models.Model):
    page = ParentalKey(
        "PostPage",
        related_name="post_person_relationship",
        on_delete=models.CASCADE,
    )

    person = models.ForeignKey(
        "base.Person",
        related_name="person_post_relationship",
        on_delete=models.CASCADE,
    )

    panels = [FieldPanel("person")]


class ArchivePage(RoutablePageMixin, Page):
    subpage_types = ["PostPage"]
    POSTS_PER_PAGE = 5

    @re_path(r"^(\d{4})/(\d{2})/(\d{2})/(.+)/$", name="archive")
    def archive_by_date_slug(self, request, year, month, day, slug):
        """
        Route for individual archive: /yyyy/mm/dd/slug/
        """

        try:
            year, month, day = int(year), int(month), int(day)
        except ValueError:
            raise Http404("Invalid date format")

        post = get_object_or_404(
            PostPage.objects.live().public(),  # type: ignore
            slug=slug,
            first_published_at__year=year,
            first_published_at__month=month,
            first_published_at__day=day,
        )

        return post.specific.serve(request)

    @re_path(r"^authors/(?P<author_slug>[\w-]+)/$", name="posts_by_author")
    @re_path(
        r"^authors/(?P<author_slug>[\w-]+)/page/(?P<page>\d+)/$",
        name="posts_by_author_paginated",
    )
    def posts_by_author(self, request, author_slug, page=1):
        """Posts by specific author with pagination"""

        try:
            author = Person.objects.get(slug=author_slug)
        except Person.DoesNotExist:
            raise Http404("Author not found")

        posts = (
            self._get_posts_queryset()
            .filter(post_person_relationship__person=author)
            .distinct()
        )

        if not posts.exists():
            raise Http404(f"No posts found for author '{author_slug}'")

        paginated_posts = self._paginate_posts(
            request, posts, page_number=page, base_url=f"/archive/authors/{author_slug}"
        )

        context = self.get_context(request, paginated_posts=paginated_posts)

        context["posts"] = paginated_posts
        context["author"] = author

        return self.render(request, context_overrides=context)

    @re_path(r"^$")
    @re_path(r"^page/(?P<page>\d+)/$")
    def paginated_posts(self, request, page=1):
        """Main archive page with pagination"""
        posts = self._get_posts_queryset()
        paginated_posts = self._paginate_posts(
            request, posts, page_number=page, base_url="/archive"
        )

        context = self.get_context(request, paginated_posts=paginated_posts)
        context["posts"] = paginated_posts

        return self.render(request, context_overrides=context)

    def _get_posts_queryset(self):
        """Base queryset for all posts"""
        return (
            PostPage.objects.child_of(self)  # type: ignore
            .live()
            .public()
            .order_by("-first_published_at")
        )

    def _build_page_url(self, base_url, page_num):
        """Helper to build page URLs consistently"""
        if page_num == 1:
            return f"{base_url}/"
        return f"{base_url}/page/{page_num}/"

    def _paginate_posts(self, request, qs, page_number=None, base_url=None):
        """
        Generic pagination helper for any posts queryset
        Returns paginated posts object
        """

        page_number = page_number or request.GET.get("page", 1)

        paginator = Paginator(qs, self.POSTS_PER_PAGE)

        try:
            page_number = int(page_number)
        except (ValueError, TypeError):
            raise Http404("Invalid page number")

        try:
            paginated_posts = paginator.page(page_number)
        except (PageNotAnInteger, EmptyPage):
            raise Http404("Invalid or missing page")

        if not base_url:
            return paginated_posts

        paginated_posts.next = (  # type: ignore
            self._build_page_url(base_url, paginated_posts.next_page_number())
            if paginated_posts.has_next()
            else None
        )

        paginated_posts.prev = (  # type: ignore
            self._build_page_url(base_url, paginated_posts.previous_page_number())
            if paginated_posts.has_previous()
            else None
        )

        return paginated_posts

    def get_context(self, request, paginated_posts=None, *args, **kwargs):
        """Add common context variables"""
        context = super().get_context(request, *args, **kwargs)
        context["posts_per_page"] = self.POSTS_PER_PAGE
        if paginated_posts:
            context["next_url"] = paginated_posts.next  # type: ignore
            context["prev_url"] = paginated_posts.prev  # type: ignore
        return context


class PostPage(SeoMetaFields, Page):  # type: ignore
    body = StreamField(
        [
            ("note", NoteBlock()),
            ("article", ArticleBlock()),
            ("reply", ReplyBlock()),
            ("like", LikeBlock()),
            ("repost", RepostBlock()),
            ("bookmark", BookmarkBlock()),
            ("photo", PhotoBlock()),
            ("video", VideoBlock()),
        ],
        use_json_field=True,
        default="article",
        min_num=1,
        max_num=1,
    )

    parent_page_types = ["ArchivePage"]
    subpage_types = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.pk:
            timestamp = now().strftime("%H%M%S")
            self.title = timestamp
            self.slug = timestamp

    def authors(self):
        return [
            n.person
            for n in self.post_person_relationship.filter(  # type: ignore
                person__live=True
            ).select_related("person")
        ]

    def get_url_parts(self, request=None):
        response = super().get_url_parts(request)
        if response is None:
            return None

        site_id, root_url, _ = response

        post_path = self._get_post_path()
        if post_path is None:
            return None

        return (site_id, root_url, f"/archive/{post_path}")

    def _get_post_path(self):
        if not self.first_published_at or not self.slug:
            return None

        parent = self.get_parent()
        if not parent:
            return None

        parent = parent.specific  # type: ignore
        return parent.reverse_subpage(  # type: ignore
            "archive",
            args=[
                self.first_published_at.strftime("%Y"),
                self.first_published_at.strftime("%m"),
                self.first_published_at.strftime("%d"),
                self.slug,
            ],
        )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
        MultipleChooserPanel(
            "post_person_relationship",
            chooser_field_name="person",
            heading="Authors",
            label="Author",
            panels=None,
            min_num=1,
        ),
    ]
