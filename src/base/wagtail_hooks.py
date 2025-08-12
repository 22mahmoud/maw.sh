from django.urls import reverse
from wagtail import hooks
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    MultiFieldPanel,
    PublishingPanel,
)
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtailmenus.models.menus import MainMenu

from .models import Person, Technology


class PersonViewSet(SnippetViewSet):
    model = Person
    menu_label = "People"  # type: ignore
    icon = "group"  # type: ignore
    list_display = ("first_name", "last_name", "title", "thumb_image")  # type: ignore
    panels = [
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("first_name"),
                        FieldPanel("last_name"),
                    ]
                )
            ],
            "Name",
        ),
        FieldPanel("slug"),
        MultiFieldPanel(
            [
                FieldPanel("title"),
                FieldPanel("bio"),
            ],
            "Info",
        ),
        FieldPanel("image"),
        PublishingPanel(),
    ]


class TechnologyViewSet(SnippetViewSet):
    model = Technology
    menu_label = "Technology"  # type: ignore
    icon = "code"  # type: ignore
    list_display = ("name", "thumb_icon")  # type: ignore
    panels = [
        FieldPanel("name"),
        FieldPanel("icon"),
    ]


register_snippet(PersonViewSet)
register_snippet(TechnologyViewSet)


@hooks.register("menus_modify_primed_menu_items")  # type: ignore
def modify_primed_menu_items(menu_items, request, **kwargs):
    menu_instance = kwargs.get("menu_instance")

    if not isinstance(menu_instance, MainMenu):
        return menu_items

    for item in menu_items:
        item.url = item.href
        item.variant = "nav_active" if bool(item.active_class) else "nav"

    if request.user.is_authenticated:
        menu_items.append(
            {
                "url": reverse("account_profile"),
                "text": "Profile",
                "variant": "auth",
            }
        )
    else:
        menu_items.append(
            {
                "url": reverse("account_login"),
                "text": "Sign in",
                "variant": "auth",
            }
        )
    return menu_items
