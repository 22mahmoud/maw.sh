from django import template

from src.base.constants import SOCIAL_PLATFORMS
from src.base.models import SiteSettings

register = template.Library()


@register.simple_tag(takes_context=True)
def get_social_data(context, value_struct):
    request = context.get("request")
    if not request:
        return {}

    settings = SiteSettings.for_request(request)

    key = value_struct.get("platform")

    if not key:
        return {}

    handle = getattr(settings, key, None)
    if not handle:
        return {}

    info = SOCIAL_PLATFORMS[key]

    value_struct["url"] = info["url_pattern"].format(handle)
    value_struct["icon"] = info["icon"]
    value_struct["sr_text"] = info["label"]

    return value_struct
