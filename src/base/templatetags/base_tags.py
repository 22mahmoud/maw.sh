import re
from urllib.parse import urlparse

import markdown
from django import template
from django.forms.utils import flatatt
from django.template.defaultfilters import stringfilter
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
        "class": attrs.get("class", None),
        "fill": attrs.get("fill", "currentColor"),
    }

    template_name = f"icons/{name}.html"

    try:
        svg_content = render_to_string(template_name, context)
        return mark_safe(svg_content)
    except TemplateDoesNotExist:
        return ""


def allow_src(tag, name, value):
    if name in ("alt", "height", "width"):
        return True
    if name == "src":
        p = urlparse(value)
        allowed_domains = (".giphy.com", ".tenor.com", ".imgur.com")
        return not p.netloc or any(
            p.netloc.endswith(domain) for domain in allowed_domains
        )

    return False


ALLOWED_ATTRS = {"a": ["href"], "img": allow_src}

ALLOWED_TAGS = [
    "p",
    "br",
    "strong",
    "em",
    "code",
    "pre",
    "ul",
    "ol",
    "li",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "img",
]


@register.filter
@stringfilter
def render_markdown(value):
    md = markdown.Markdown(extensions=["fenced_code"])
    html_output = md.convert(value)
    return mark_safe(html_output)
