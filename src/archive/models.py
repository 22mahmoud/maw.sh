from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
from wagtail.models.pages import StreamField
from wagtail.contrib.routable_page.models import RoutablePageMixin, re_path

from .blocks import (
    NoteBlock,
    ArticleBlock,
    ReplyBlock,
    RepostBlock,
    BookmarkBlock,
    PhotoBlock,
    VideoBlock,
    LikeBlock,
)


class ArchivePage(RoutablePageMixin, Page):
    subpage_types = ["PostPage"]

    @re_path(r"^(\d{4})/(\d{2})/(\d{2})/(.+)/$", name="archive")
    def archive_by_date_slug(self, request, year, month, day, slug):
        """
        Route for individual archive: /yyyy/mm/dd/slug/
        """

        year, month, day = int(year), int(month), int(day)

        post = get_object_or_404(
            PostPage.objects.live().public(),  # type: ignore
            slug=slug,
            first_published_at__year=year,
            first_published_at__month=month,
            first_published_at__day=day,
        )

        return post.serve(request)

    def _get_posts_queryset(self):
        return (
            PostPage.objects.child_of(self)  # type: ignore
            .live()
            .public()
            .order_by("-first_published_at")
        )

    def serve_preview(self, request, mode_name):
        # Needed for previews to work
        return self.serve(request)

    @re_path(r"^$")
    @re_path(r"^page/(?P<page>\d+)/$")
    def paginated_posts(self, request, page=1):
        posts = self._get_posts_queryset()

        paginator = Paginator(posts, 3)
        try:
            paginated_posts = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            paginated_posts = paginator.page(1)

        context = self.get_context(request)
        context["posts"] = paginated_posts
        return self.render(request, context_overrides=context)


class PostPage(Page):
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

    def get_url_parts(self, request=None):
        response = super().get_url_parts(request)
        if response is None:
            return None

        site_id, root_url, _ = response

        post_path = self._get_post_path()
        if post_path is None:
            return None

        return (site_id, root_url, f"/archive/{post_path}")

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
