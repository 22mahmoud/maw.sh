from django.contrib.contenttypes.models import ContentType
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from wagtail.contrib.search_promotions.models import Query
from wagtail.models import Page

from src.pagination.mixins import PaginatedArchiveMixin
from src.posts.models import BasePostPage
from src.utils.get_subclasses import get_all_subclasses


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
        queryset = Page.objects.none()

        if search_query:
            post_page_subclasses = get_all_subclasses(BasePostPage)

            if post_page_subclasses:
                content_types = [
                    ContentType.objects.get_for_model(cls)
                    for cls in post_page_subclasses
                ]

                queryset = (
                    Page.objects.live()  # type:ignore
                    .filter(content_type__in=content_types)
                    .specific()
                    .search(search_query)
                )

            Query.get(search_query).add_hit()

        page_number = request.GET.get("page", "1")

        try:
            paginated_results = self.paginate_posts(
                qs=queryset,
                page_number=int(page_number),
            )
        except Http404:
            paginated_results = None

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
