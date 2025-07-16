from django import template
from django.forms.utils import flatatt
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from src.utils.cva import cva

register = template.Library()

INPUT_CVA = cva(
    base=(
        "peer w-full bg-neutral-800 px-3 py-2 text-primary shadow-md "
        "transition-colors placeholder:text-secondary focus:outline-none"
    ),
    variants={
        "state": {
            "default": (
                "border border-neutral-700 "
                "focus:border-accent focus:ring-1 focus:ring-accent/50"
            ),
            "error": (
                "border border-red-500 text-red-500 placeholder:text-red-500/70 "
                "focus:border-red-500 focus:ring-1 focus:ring-red-500/50"
            ),
        }
    },
    default_variants={"state": "default"},
)

LABEL_CVA = cva(
    base="block text-base transition-colors",
    variants={
        "state": {
            "default": "text-primary peer-focus:text-accent",
            "error": "text-red-500",
        }
    },
    default_variants={"state": "default"},
)


class FormFieldNode(template.Node):
    def __init__(self, kwargs):
        self.kwargs = kwargs

    def render(self, context):
        resolved = {key: val.resolve(context) for key, val in self.kwargs.items()}

        name = resolved.get("name")
        value = resolved.get("value", "")
        if not name:
            raise template.TemplateSyntaxError(
                "The 'field' tag requires a 'name' attribute."
            )

        tag_type = resolved.get("as", "input")
        label_text = resolved.get("label", name.replace("_", " ").title())
        has_error = resolved.get("error", False)
        error_message = resolved.get("error_message", None)
        user_class = resolved.get("class", "")

        state = "error" if has_error else "default"

        input_class = f"{INPUT_CVA({'state': state})} {user_class}".strip()
        label_class = LABEL_CVA({"state": state})

        attrs = resolved.copy()
        attrs["id"] = resolved.get("id", name)
        attrs["class"] = input_class

        keys_to_remove = ["label", "error", "error_message", "as_textarea"]
        for key in keys_to_remove:
            attrs.pop(key, None)

        attrs = {k.replace("_", "-"): v for k, v in attrs.items()}

        return render_to_string(
            "includes/field.html",
            {
                "name": name,
                "label_text": label_text,
                "label_class": label_class,
                "has_error": has_error,
                "error_message": error_message,
                "tag_type": tag_type,
                "value": value or "",
                "field_attrs": mark_safe(flatatt(attrs)),
            },
        )


@register.tag
def field(parser, token):
    """
    Renders a form field with a label, input/textarea, and error message.

    Usage:
        {% field name="email" type="email" label="Your Email" %}

        {% field name="message" label="Your Message" as="textarea" rows=4 %}

    With errors:
        {% field name="email" type="email" error=form.email.errors error_message=form.email.errors.as_text %}
    """
    bits = token.split_contents()[1:]
    kwargs = {}
    for bit in bits:
        if "=" in bit:
            key, value = bit.split("=", 1)
            kwargs[key] = parser.compile_filter(value)
        else:
            raise template.TemplateSyntaxError(
                f"Invalid argument '{bit}' in 'field' tag. Arguments must be key=value pairs."
            )

    return FormFieldNode(kwargs)
