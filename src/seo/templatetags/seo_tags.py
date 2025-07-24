from contextlib import suppress
from typing import TYPE_CHECKING, Any

from django import template
from wagtail.models import Page

from src.seo.models import SeoSettings

if TYPE_CHECKING:
    from django.http import HttpRequest

register = template.Library()


@register.simple_tag(takes_context=True)
def seo_full_title(context: dict[str, Any], page: Page) -> str:
    """Generates SEO title with suffix from settings."""

    title = ""

    if hasattr(page, "seo_title") and page.seo_title:
        title = page.seo_title
    elif hasattr(page, "title") and page.title:
        title = page.title
    elif context.get("page") and context["page"].get("seo_title"):
        title = context["page"]["seo_title"]
    elif context.get("page") and context["page"].get("title"):
        title = context["page"]["title"]

    title = title.strip()
    suffix = ""

    request: HttpRequest | None = context.get("request")
    if not request:
        return title

    settings = None
    with suppress(Exception):
        settings = SeoSettings.for_request(request)

    if not settings or not hasattr(settings, "title_suffix") or not settings.title_suffix:
        return title

    suffix = f" | {settings.title_suffix.strip()}"

    return f"{title}{suffix}"


@register.simple_tag
def seo_meta_description(page: Page) -> str:
    """Returns search description if available."""

    return getattr(page, "search_description", "")
