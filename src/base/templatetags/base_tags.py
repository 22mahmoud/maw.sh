import re

from django import template
from django.forms.utils import flatatt
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

    attrs = {}

    attrs["fill"] = "currentColor"
    attrs.update(kwargs)

    attrs = {k.replace("_", "-"): v for k, v in attrs.items()}

    context = {
        "attrs": mark_safe(flatatt(attrs)),
        "class": attrs.get("class"),
        "fill": attrs.get("fill", "currentColor"),
    }

    template_name = f"icons/{name}.html"

    try:
        svg_content = render_to_string(template_name, context)
        return mark_safe(svg_content)
    except TemplateDoesNotExist:
        return ""
