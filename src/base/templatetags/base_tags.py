import ast
import json
from django import template
from django.template.loader import get_template, TemplateDoesNotExist
from importlib import import_module

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
    icon_path = f"icons/{name}.svg"
    try:
        get_template(icon_path)
        return icon_path
    except TemplateDoesNotExist:
        return fallback


@register.simple_tag
def make_dict(**kwargs):
    return kwargs


@register.simple_tag
def resolve_classes(block, cva_key, props=None, **kwargs):
    module = import_module(block)

    get_cva = getattr(module, "get_cva", None)
    if not callable(get_cva):
        return ""

    cva_fn = get_cva(cva_key)
    if not callable(cva_fn):
        return ""

    props = props or {}
    props.update(kwargs)
    return cva_fn(props)
