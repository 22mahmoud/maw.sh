from django import template

from src.base.models import SiteSettings

register = template.Library()


@register.simple_tag(takes_context=True)
def get_social_data(context, platform_info):
    request = context.get("request")
    if not request:
        return {}

    settings = SiteSettings.for_request(request)
    platform_key = platform_info.get("key")

    if not platform_key:
        return {}

    handle = getattr(settings, platform_key, None)
    if not handle:
        return {}

    return {
        "url": platform_info["url_pattern"].format(handle),
        "icon": platform_info["icon"],
        "platform": platform_key,
    }
