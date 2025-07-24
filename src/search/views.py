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

        if page_num > 1:
            query_params["page"] = str(page_num)
        elif "page" in query_params:
            del query_params["page"]

        if query_params:
            return f"{self.request.path}?{query_params.urlencode()}"
        else:
            return self.request.path

    def get(self, request: HttpRequest) -> HttpResponse:
        search_query = request.GET.get("q", None)

        if search_query:
            search_query = search_query.strip()
        if not search_query:
            search_query = None

        if search_query:
            queryset = Page.objects.live().specific().search(search_query)  # type: ignore
            Query.get(search_query).add_hit()
        else:
            queryset = Page.objects.none()

        page_number = request.GET.get("page", "1")

        paginated_results = self.paginate_posts(
            qs=queryset,
            page_number=int(page_number),
        )

        context = self.get_paginated_context(
            request, paginated_posts=paginated_results, search_query=search_query
        )

        context["type"] = "search"
        context["page"] = {}
        context["page"]["title"] = "Search"

        if search_query:
            total_results = paginated_results.paginator.count  # type: ignore
            context["page"]["introduction"] = (
                f"{total_results} result{'s' if total_results != 1 else ''} found for '{search_query}'."
            )

            context["page"]["seo_title"] = f"Search: {search_query}"

            if total_results == 0:
                context["empty_state_message"] = (
                    f"No results found for '{search_query}'."
                )
        else:
            context["page"]["introduction"] = (
                "Enter a search query to explore the archive."
            )
            context["empty_state_message"] = (
                "No posts to display. Try entering a search query."
            )

        return render(request, self.template_name, context)
