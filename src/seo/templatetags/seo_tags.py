from contextlib import suppress
from typing import TYPE_CHECKING, Any

from django import template
from wagtail.models import Page

from src.seo.models import SeoSettings

if TYPE_CHECKING:
    from django.http import HttpRequest

register = template.Library()


@register.simple_tag(takes_context=True)
def seo_full_title(context: dict[str, Any], page: Page | None = None) -> str:
    """Generates SEO title with suffix from settings."""

    title = ""

    if page:
        raw_title = getattr(page, "seo_title", None) or getattr(page, "title", None)
    else:
        raw_page = context.get("page")
        raw_title = None
        if isinstance(raw_page, dict):
            raw_title = raw_page.get("seo_title") or raw_page.get("title")
        elif raw_page:
            raw_title = getattr(raw_page, "seo_title", None) or getattr(raw_page, "title", None)

    # Sanitize the title
    if callable(raw_title):
        title = raw_title()
    elif isinstance(raw_title, str):
        title = raw_title
    elif raw_title:
        title = str(raw_title)

    title = title.strip() if isinstance(title, str) else ""

    request: HttpRequest | None = context.get("request")
    if not request:
        return title

    suffix = ""
    with suppress(Exception):
        settings = SeoSettings.for_request(request)
        if settings and getattr(settings, "title_suffix", None):
            suffix = f" | {settings.title_suffix.strip()}"

    return f"{title}{suffix}" if title else suffix


@register.simple_tag
def seo_meta_description(page: Page) -> str:
    """Returns search description if available."""

    return getattr(page, "search_description", "")
