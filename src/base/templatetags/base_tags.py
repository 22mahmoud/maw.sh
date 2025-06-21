import ast
import json
from django import template
from django.template.loader import get_template, TemplateDoesNotExist

register = template.Library()


@register.filter("smart_deserialize")
def smart_deserialize(value):
    if isinstance(value, dict):
        return value

    if not isinstance(value, str):
        return {}

    try:
        return json.loads(value)
    except (json.JSONDecodeError, ValueError):
        pass

    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        pass

    return {}


@register.simple_tag
def get_icon(name, fallback="icons/default.svg"):
    print(name)
    icon_path = f"icons/{name}.svg"
    try:
        get_template(icon_path)
        return icon_path
    except TemplateDoesNotExist:
        return fallback
