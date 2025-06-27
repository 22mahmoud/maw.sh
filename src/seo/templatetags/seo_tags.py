from typing import Any, Dict, Optional

from django import template
from django.http import HttpRequest
from wagtail.models import Page

from src.seo.models import SeoSettings

register = template.Library()


@register.simple_tag(takes_context=True)
def seo_full_title(context: Dict[str, Any], page: Page) -> str:
    """Generates SEO title with suffix from settings."""

    title = (getattr(page, "seo_title", None) or getattr(page, "title", "")).strip()
    suffix = ""

    request: Optional[HttpRequest] = context.get("request")
    if not request:
        return title

    settings = None
    try:
        settings = SeoSettings.for_request(request)
    except Exception:
        pass

    if (
        not settings
        or not hasattr(settings, "title_suffix")
        or not settings.title_suffix
    ):
        return title

    suffix = f" | {settings.title_suffix.strip()}"

    return f"{title}{suffix}"


@register.simple_tag
def seo_meta_description(page: Page) -> str:
    """Returns search description if available."""

    return getattr(page, "search_description", "")
