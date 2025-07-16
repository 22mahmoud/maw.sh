import re

from django import template
from django.template.loader import TemplateDoesNotExist, render_to_string
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def strip_p_tags(value):
    return re.sub(r"</?p[^>]*>", "", value)


@register.simple_tag
def icon(name: str, **kwargs):
    if not name:
        return ""

    template_name = f"icons/{name}.svg"

    try:
        svg_content = render_to_string(template_name, kwargs)
        return mark_safe(svg_content)
    except TemplateDoesNotExist:
        return ""
