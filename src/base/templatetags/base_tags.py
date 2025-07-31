import re

from django import template
from django.forms import widgets
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


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def message_color(tags):
    if "error" in tags:
        return "bg-[#2d2d2d] text-red-400 border-s-red-500"
    if "warning" in tags:
        return "bg-[#2d2d2d] text-orange-400 border-s-orange-500"
    if "success" in tags:
        return "bg-[#2d2d2d] text-green-400 border-s-green-500"
    if "info" in tags:
        return "bg-[#2d2d2d] text-blue-400 border-s-blue-500"
    return "bg-[#2d2d2d] text-primary border-s-neutral-700"


@register.filter
def widget_type(field):
    widget = field.field.widget
    if isinstance(widget, widgets.Textarea):
        return "textarea"
    if isinstance(widget, widgets.TextInput):
        return "input"
    if isinstance(widget, widgets.CheckboxInput):
        return "checkbox"
    if isinstance(widget, widgets.Select):
        return "select"
    return "input"
