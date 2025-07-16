from wagtail import hooks
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    MultiFieldPanel,
    PublishingPanel,
)
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import Person


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


register_snippet(PersonViewSet)


@hooks.register("menus_modify_primed_menu_items")  # type: ignore
def make_some_changes(menu_items, **_):
    for item in menu_items:
        item.text = item.text
        item.url = item.href
        item.variant = "nav_active" if bool(item.active_class) else "nav"

    return menu_items
