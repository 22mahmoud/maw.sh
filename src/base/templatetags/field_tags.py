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
                "border border-neutral-700 focus:border-accent focus:ring-1 focus:ring-accent/50"
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


class FieldBlockNode(template.Node):
    def __init__(self, nodelist, kwargs):
        self.nodelist = nodelist
        self.kwargs = kwargs

    def render(self, context):
        resolved = {key: val.resolve(context) for key, val in self.kwargs.items()}
        content = self.nodelist.render(context)

        name = resolved.get("name")
        value = resolved.get("value", "")
        if not name:
            raise template.TemplateSyntaxError("The 'field' tag requires a 'name' attribute.")

        tag_type = resolved.get("as", "input")
        label_text = resolved.get("label")
        has_error = resolved.get("error", False)
        error_message = resolved.get("error_message", "")
        help_text = resolved.get("help_text", "")
        user_class = resolved.get("class", "")

        state = "error" if has_error else "default"

        if tag_type == "checkbox":
            input_class = (
                f"accent-accent w-5 h-5 rounded border border-neutral-700 {user_class}".strip()
            )
        elif tag_type == "radio":
            input_class = f"accent-accent w-5 h-5 border border-neutral-700 {user_class}".strip()
        else:
            input_class = f"{INPUT_CVA({'state': state})} {user_class}".strip()

        label_class = LABEL_CVA({"state": state})

        attrs = resolved.copy()
        attrs["id"] = resolved.get("id", name)
        attrs["class"] = input_class
        attrs["aria-invalid"] = "true" if has_error else "false"

        error_id = f"{attrs['id']}-error"
        if error_message:
            attrs["aria-describedby"] = error_id

        # Clean up
        for key in ["label", "error", "error_message", "help_text"]:
            attrs.pop(key, None)

        attrs = {k.replace("_", "-"): v for k, v in attrs.items()}

        return render_to_string(
            "includes/field.html",
            {
                "id": attrs["id"],
                "name": name,
                "label_text": label_text,
                "label_class": label_class,
                "error_id": error_id,
                "error_message": error_message,
                "help_text": help_text,
                "tag_type": tag_type,
                "value": value or "",
                "field_attrs": mark_safe(flatatt(attrs)),
                "options_html": mark_safe(content),
            },
        )


@register.tag()
def field(parser, token):
    nodelist = parser.parse(("endfield",))
    parser.delete_first_token()

    bits = token.split_contents()[1:]
    kwargs = {}

    for bit in bits:
        if "=" in bit:
            key, value = bit.split("=", 1)
            kwargs[key] = parser.compile_filter(value)

    return FieldBlockNode(nodelist, kwargs)


@register.simple_tag
def input_class(state="default", user_class=""):
    return f"{INPUT_CVA({'state': state})} {user_class}".strip()


@register.simple_tag
def label_class(state="default"):
    return LABEL_CVA({"state": state})
