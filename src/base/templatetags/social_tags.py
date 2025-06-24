from django import template

from src.base.constants import SOCIAL_PLATFORMS
from src.base.models import SiteSettings

register = template.Library()


@register.simple_tag(takes_context=True)
def get_social_data(context, key):
    request = context.get("request")
    if not request:
        return {}

    settings = SiteSettings.for_request(request)

    if not key:
        return {}

    handle = getattr(settings, key, None)
    if not handle:
        return {}

    info = SOCIAL_PLATFORMS[key]

    return {
        "url": info["url_pattern"].format(handle),
        "icon": info["icon"],
        "platform": info["key"],
        "sr_text": info["label"],
    }
