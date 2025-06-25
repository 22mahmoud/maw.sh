from typing import Optional
from django import template
from django.http import HttpRequest
from wagtail.models import Site

register = template.Library()


@register.simple_tag(takes_context=True)
def get_site_root(context):
    request: Optional[HttpRequest] = context.get("request")
    return Site.find_for_request(request).root_page  # type: ignore


@register.inclusion_tag("tags/top_menu.html", takes_context=True)
def top_menu(context, parent=None, source=None):
    menuitems = (parent or get_site_root(context)).get_children().live().in_menu()

    for menuitem in menuitems:
        menuitem.text = menuitem.title
        menuitem.active = (
            source.url_path.startswith(menuitem.url_path) if source else False
        )
        menuitem.props = {
            "variant": "nav_active" if menuitem.active else "nav_inactive"
        }

    return {
        "source": source,
        "menuitems": menuitems,
        "request": context["request"],
    }
