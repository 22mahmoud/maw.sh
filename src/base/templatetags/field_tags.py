from posixpath import basename
from typing import TYPE_CHECKING, Any, TypedDict

from django import template
from django.forms import BoundField
from django.forms.utils import ErrorList
from django.template.loader import render_to_string
from django.utils.html import escape
from django.utils.safestring import mark_safe

from src.base.templatetags.base_tags import widget_type
from src.utils.cva import cva

if TYPE_CHECKING:
    from django.core.files import File
    from django.db.models import Model

register = template.Library()


def render_attrs(attrs):
    attrs = {k: (k if v is True else v) for k, v in attrs.items() if v not in [None, False]}

    return mark_safe(
        " ".join(
            f'{escape(key)}="{escape(value)}"' for key, value in attrs.items() if value is not None
        )
    )


INPUT_CVA = cva(
    base=(
        "peer w-full bg-neutral-800 px-3 py-2 text-primary shadow-md "
        "border border-neutral-700 placeholder:text-secondary "
        "transition-colors focus:outline-none "
        "focus:border-accent focus:ring-1 focus:ring-accent/50 "
        "aria-invalid:border-red-500 aria-invalid:text-red-500 "
        "aria-invalid:placeholder:text-red-500/70 "
        "aria-invalid:focus:border-red-500 aria-invalid:focus:ring-red-500/50"
    ),
    variants={
        "as": {
            "input": "",
            "textarea": "min-h-[120px]",
            "checkbox": "accent-accent w-5! h-5! shadow-none! rounded border border-neutral-700",
            "radio": "accent-accent w-5 h-5 border border-neutral-700 rounded-full",
            "file": "",
        },
    },
    default_variants={"as": "input"},
)

LABEL_CVA = cva(
    base=(
        "block text-base text-primary transition-colors "
        "peer-focus:text-accent peer-aria-invalid:text-red-500"
    )
)


class FieldContext(TypedDict):
    id: str | None
    name: str | None
    value: str | None
    label: str | None
    help_text: str | None
    errors: ErrorList | list[str] | None
    type: str | None
    disabled: bool | None
    required: bool | None
    tag_type: str | None
    field_attrs: str | None
    content: Any
    wrapper_class: str | None
    wrapper_attrs: str | None
    label_class: str | None
    file_url: str | None
    file_name: str | None


non_html_keys = {
    "id",
    "name",
    "label",
    "errors",
    "help_text",
    "wrapper_class",
    "label_class",
    "class",
    "as",
    "tag_type",
    "field",
    "wrapper_attrs",
    "wrapper",
}


class FieldBlockNode(template.Node):
    def __init__(self, nodelist, kwargs):
        self.nodelist = nodelist
        self.kwargs = kwargs

    def render(self, context):
        ctx: FieldContext = {
            "id": None,
            "name": None,
            "value": "",
            "label": "",
            "type": "text",
            "help_text": "",
            "errors": None,
            "disabled": None,
            "required": None,
            "tag_type": "input",
            "field_attrs": "",
            "content": "",
            "wrapper_class": "",
            "label_class": "",
            "wrapper_attrs": None,
            "file_name": None,
            "file_url": None,
        }

        # 1. resolve the kwargs
        resolved = {k: v.resolve(context) for k, v in self.kwargs.items()}

        # 2. get the content if exists
        content = self.nodelist.render(context)

        # 3. pre-fill the resolved with bound filed if exists
        field: BoundField | None = resolved.get("field")
        if isinstance(field, BoundField):
            widget_attrs = getattr(field.field.widget, "attrs", {}) or {}
            resolved.update(
                {
                    "disabled": "disabled" if field.field.disabled else None,
                    "required": "required" if field.field.required else None,
                    "type": getattr(field.field.widget, "input_type", "text"),
                    "value": field.value(),
                    "id": field.id_for_label,
                    "name": field.name,
                    "label": field.label,
                    "help_text": field.help_text,
                    "errors": field.errors,
                    "checked": True if field.widget_type == "checkbox" and field.value() else None,  # type: ignore
                    "as": resolved.get("as", widget_type(field)),  # type: ignore
                    **widget_attrs,
                }
            )

        # 4. compute required fields
        name = resolved.get("name", ctx["name"])
        if not name:
            raise template.TemplateSyntaxError(
                "The 'field' tag requires either a 'field' or 'name' attribute."
            )

        tag_type = resolved.get("as")
        has_error = bool(resolved.get("errors"))
        help_text = resolved.get("help_text")
        id = resolved.get("id", name)
        label = resolved.get("label")
        wrapper_attrs = resolved.get("wrapper", {})

        # - compute classes
        user_class = resolved.get("class", "")
        wrapper_class = wrapper_attrs.get("class", "") or resolved.get("wrapper_class", "")
        input_class = f"{INPUT_CVA({'as': tag_type})} {user_class}".strip()
        label_class = LABEL_CVA({})

        # build attrs and sanitize it
        attrs = resolved.copy()

        for key in non_html_keys:
            attrs.pop(key, None)

        if tag_type == "textarea":
            attrs.pop("value", None)

        attrs["class"] = input_class
        attrs["id"] = id
        attrs["name"] = name
        attrs["aria-invalid"] = str(has_error).lower()
        attrs["aria-errormessage"] = f"{id}-error" if has_error else None
        attrs["aria-describedby"] = f"{id}-help" if help_text else None

        ctx["id"] = id
        ctx["name"] = name
        ctx["label"] = label
        ctx["help_text"] = help_text
        ctx["label_class"] = label_class
        ctx["wrapper_class"] = wrapper_class
        ctx["field_attrs"] = render_attrs(attrs)
        ctx["wrapper_attrs"] = render_attrs(wrapper_attrs)
        ctx["content"] = content
        ctx["tag_type"] = tag_type
        ctx["type"] = attrs["type"]

        if resolved.get("type") == "file" and field:
            instance: Model = getattr(field.form, "instance")
            file: File | None = getattr(instance, name, None)

            if file:
                file_url: str = getattr(file, "url", "")
                file_name: str = basename(getattr(file, "name", ""))

                ctx["file_url"] = file_url
                ctx["file_name"] = file_name

        # 5. render template
        return render_to_string(
            "includes/field.html",
            ctx,  # type: ignore
        )


@register.tag()
def field(parser, token):
    bits = token.split_contents()[1:]
    nodelist = parser.parse(("endfield",))
    parser.delete_first_token()

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
