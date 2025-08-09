from django.core.paginator import (
    EmptyPage,
    PageNotAnInteger,
    Paginator,
)
from django.core.paginator import (
    Page as PaginatorPage,
)
from django.http import Http404


class PaginatedArchiveMixin:
    POSTS_PER_PAGE = 10

    def get_posts_queryset(self):
        raise NotImplementedError("Subclasses must implement get_posts_queryset()")

    def get_posts_per_page(self):
        return getattr(self, "POSTS_PER_PAGE", 10)

    def build_page_url(self, page_num: int, base_url=None):
        base_url = (base_url or self.url).rstrip("/")  # type: ignore

        return f"{base_url}/" if page_num == 1 else f"{base_url}/page/{page_num}/"

    def paginate_posts(self, qs, page_number: int | None = None, base_url=None) -> PaginatorPage:
        if not page_number:
            raise Http404("missing page")

        paginator = Paginator(qs, self.get_posts_per_page())

        try:
            page_number = int(page_number)
        except (ValueError, TypeError):
            raise Http404("Invalid page number")

        try:
            paginated_posts = paginator.page(page_number)
        except (PageNotAnInteger, EmptyPage):
            raise Http404("Invalid or missing page")

        self._add_navigation_urls(paginated_posts, base_url=base_url)

        return paginated_posts

    def _add_navigation_urls(self, paginated_posts: PaginatorPage, base_url=None) -> None:
        paginated_posts.next = (  # type: ignore
            self.build_page_url(paginated_posts.next_page_number(), base_url)
            if paginated_posts.has_next()
            else None
        )

        paginated_posts.prev = (  # type: ignore
            self.build_page_url(paginated_posts.previous_page_number(), base_url)
            if paginated_posts.has_previous()
            else None
        )

    def get_paginated_context(self, request, paginated_posts=None, **kwargs):
        context = self.get_context(request, **kwargs)  # type: ignore

        if paginated_posts:

            def full(url):
                return request.build_absolute_uri(url) if url else None

            context["posts"] = paginated_posts
            context["next_url"] = full(getattr(paginated_posts, "next", None))
            context["prev_url"] = full(getattr(paginated_posts, "prev", None))

        return context
