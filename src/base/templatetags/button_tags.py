from django import template
from django.utils.safestring import mark_safe

from src.base.blocks.button import DEFAULT_BUTTON_SIZE, DEFAULT_BUTTON_TYPE
from src.utils.cva import cva

BUTTON_CVA = cva(
    base=(
        "group relative inline-block cursor-pointer shadow-xs focus-visible:outline-2 "
        "focus-visible:outline-offset-2 focus-visible:outline-accent-bright"
    ),
    variants={
        "variant": {
            "primary": "text-darker font-bold",
            "secondary": "bg-neutral-800 text-primary hover:bg-neutral-700 font-medium",
            "outline": (
                "border-2 border-accent-bright text-primary bg-transparent "
                "transition-colors duration-200 hover:bg-accent-bright hover:text-black"
            ),
            "muted": (
                "text-neutral-300 hover:text-primary hover:bg-neutral-800 "
                "border border-neutral-700 hover:border-neutral-500 font-medium "
                "transition-colors duration-200"
            ),
            "disabled": (
                "bg-neutral-800 text-secondary border border-neutral-700 "
                "opacity-50 cursor-not-allowed pointer-events-none"
            ),
        },
        "size": {
            "sm": "text-sm px-2 py-1 sm:px-3 sm:py-1.5",
            "md": "text-base px-3 py-1.5 sm:px-4 sm:py-2",
            "lg": "text-lg sm:text-2xl px-3 py-2 sm:px-4 sm:py-2.5",
        },
    },
    default_variants={
        "variant": "primary",
        "size": "md",
    },
)

BUTTON_ICON_CVA = cva(
    base="",
    variants={
        "variant": {
            "primary": "fill-darker",
            "secondary": "fill-primary",
            "outline": "fill-primary group-hover:fill-black",
            "muted": "fill-neutral-300 group-hover:fill-primary",
            "disabled": "fill-secondary",
        },
        "size": {
            "sm": "w-4 h-4",
            "md": "w-5 h-5",
            "lg": "w-6 h-6",
        },
    },
    default_variants={
        "variant": "primary",
        "size": "md",
    },
)

BUTTON_TEXT_CVA = cva(
    base="",
    variants={
        "variant": {
            "primary": "",
            "secondary": "font-medium",
            "outline": "font-normal sm:font-semibold",
            "muted": "font-medium",
            "disabled": "text-secondary",
        },
        "size": {
            "sm": "text-sm",
            "md": "text-base",
            "lg": "text-lg",
        },
    },
    default_variants={
        "variant": "primary",
        "size": "md",
    },
)

register = template.Library()


@register.inclusion_tag("includes/button.html")
def button(
    text: str | None = None,
    variant: str = DEFAULT_BUTTON_TYPE,
    size: str = DEFAULT_BUTTON_SIZE,
    icon: str | None = None,
    prefix_icon: str | None = None,
    suffix_icon: str | None = None,
    href: str | None = None,
    **kwargs,
):
    user_classes = kwargs.pop("class", "")

    is_icon_only = False
    if icon:
        is_icon_only = True
        text = None
        prefix_icon = None
        suffix_icon = None

    is_link = bool(href) and variant != "disabled"
    wrapper_tag = "a" if is_link else "button"

    attrs = {}
    if is_link:
        attrs["href"] = href
        attrs["role"] = "link"
    else:
        attrs["type"] = "button"
        attrs["role"] = "button"
        if variant == "disabled":
            attrs["disabled"] = True

    attrs.update(kwargs)

    if "aria-label" not in attrs:
        if is_icon_only and icon:
            attrs["aria-label"] = icon.replace("-", " ").title()
        elif text:
            attrs["aria-label"] = text

    attr_parts = [
        key if value is True else f'{key}="{value}"'
        for key, value in attrs.items()
        if value not in [False, None]
    ]

    wrapper_attrs = mark_safe(" ".join(attr_parts))

    props = {"variant": variant, "size": size}
    cva_wrapper_class = BUTTON_CVA(props)
    icon_class = BUTTON_ICON_CVA(props)
    text_class = BUTTON_TEXT_CVA(props)
    final_wrapper_class = f"{cva_wrapper_class} {user_classes}".strip()

    return {
        "text": text,
        "variant": variant,
        "icon": icon,
        "prefix_icon": prefix_icon,
        "suffix_icon": suffix_icon,
        "wrapper_tag": wrapper_tag,
        "wrapper_attrs": wrapper_attrs,
        "wrapper_class": final_wrapper_class,
        "icon_class": icon_class,
        "text_class": text_class,
    }
