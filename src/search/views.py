from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from wagtail.contrib.search_promotions.models import Query
from wagtail.models import Page

from src.pagination.mixins import PaginatedArchiveMixin


class SearchView(PaginatedArchiveMixin, View):
    template_name = "archive/archive_page.html"

    def get_context(self, _, **kwargs):
        return kwargs

    def build_page_url(self, page_num: int, base_url=None) -> str:
        query_params = self.request.GET.copy()
        query_params.pop("page", None)

        if page_num > 1:
            query_params["page"] = str(page_num)

        return (
            f"{self.request.path}?{query_params.urlencode()}"
            if query_params
            else self.request.path
        )

    def get(self, request: HttpRequest) -> HttpResponse:
        search_query = request.GET.get("q", "")
        search_query = search_query.strip() or None

        if search_query:
            queryset = Page.objects.live().specific().search(search_query)  # type: ignore
            Query.get(search_query).add_hit()
        else:
            queryset = Page.objects.none()

        paginated_results = self.paginate_posts(
            qs=queryset,
            page_number=int(request.GET.get("page", "1")),
        )

        total_results = paginated_results.paginator.count if search_query else 0

        context = self.get_paginated_context(
            request,
            paginated_posts=paginated_results,
            search_query=search_query,
        )

        context.update(
            {
                "type": "search",
                "page": {
                    "title": "Search",
                    "introduction": (
                        f"{total_results} result{'s' if total_results != 1 else ''} found for '{search_query}'."
                        if search_query
                        else "Enter a search query to explore the archive."
                    ),
                    "seo_title": f"Search: {search_query}" if search_query else None,
                },
                "empty_state_message": (
                    f"No results found for '{search_query}'."
                    if search_query and total_results == 0
                    else "No posts to display. Try entering a search query."
                    if not search_query
                    else None
                ),
            }
        )

        return render(request, self.template_name, context)
