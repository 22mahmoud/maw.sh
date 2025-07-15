from django import template
from django.utils.safestring import mark_safe

from src.utils.cva import cva

LINK_CVA = cva(
    base=(
        "inline-flex items-center gap-3 group focus-visible:outline-none focus-visible:ring "
        "focus-visible:ring-primary underline-offset-4 hover:underline"
    ),
    variants={
        "variant": {
            "default": "text-primary hover:text-accent",
            "icon": "text-primary hover:text-accent",
            "nav": "text-white hover:text-accent",
            "nav_active": "text-accent",
        },
        "size": {
            "sm": "text-sm",
            "md": "text-base",
            "lg": "text-lg",
        },
    },
    default_variants={
        "variant": "default",
        "size": "md",
    },
)

LINK_ICON_CVA = cva(
    base="transition-colors",
    variants={
        "variant": {
            "default": "fill-primary group-hover:fill-accent",
            "icon": "fill-primary group-hover:fill-accent",
            "nav": "fill-white group-hover:fill-accent",
            "nav_active": "fill-accent",
        },
        "size": {
            "sm": "w-4 h-4",
            "md": "w-6 h-6",
            "lg": "w-8 h-8",
        },
    },
    default_variants={
        "variant": "default",
        "size": "md",
    },
)

register = template.Library()


@register.inclusion_tag("includes/link.html")
def link(
    text: str | None = None,
    variant: str = "default",
    size: str = "md",
    icon: str | None = None,
    prefix_icon: str | None = None,
    suffix_icon: str | None = None,
    href: str | None = None,
    nav_active: bool = False,
    **kwargs,
):
    """
    Renders a link component with variants and flexible icon support.
    """
    user_classes = kwargs.pop("class", "")

    # Determine content structure
    is_icon_only = bool(icon) and not (text or prefix_icon or suffix_icon)

    # Prepare attributes
    attrs = {"href": href} if href else {}
    attrs.update(kwargs)

    # Handle aria-label for accessibility, especially for icon-only links
    if "aria-label" not in attrs:
        if is_icon_only and icon:
            attrs["aria-label"] = icon.replace("-", " ").title()
        elif text:
            attrs["aria-label"] = text

    # Handle aria-current for active navigation links
    if nav_active:
        attrs["aria-current"] = "page"

    attr_parts = [
        f'{key}="{value}"' for key, value in attrs.items() if value is not None
    ]
    wrapper_attrs = mark_safe(" ".join(attr_parts))

    # Handle variant for active nav state
    final_variant = "nav" if nav_active else variant

    # Compute CSS classes
    cva_props = {"variant": final_variant, "size": size}
    cva_wrapper_class = LINK_CVA(cva_props)
    cva_icon_class = LINK_ICON_CVA(cva_props)

    # Special handling for active nav links to override hover styles
    if nav_active:
        cva_wrapper_class = cva_wrapper_class.replace(
            "hover:text-accent", "text-accent"
        )
        cva_icon_class = cva_icon_class.replace(
            "group-hover:fill-accent", "fill-accent"
        )

    final_wrapper_class = f"{cva_wrapper_class} {user_classes}".strip()

    return {
        "text": text,
        "icon": icon,
        "prefix_icon": prefix_icon,
        "suffix_icon": suffix_icon,
        "wrapper_attrs": wrapper_attrs,
        "wrapper_class": final_wrapper_class,
        "icon_class": cva_icon_class,
    }
