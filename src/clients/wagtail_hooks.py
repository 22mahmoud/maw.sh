from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import Client


class ClientViewSet(SnippetViewSet):
    model = Client
    add_to_admin_menu = True
    menu_label = "Clients"  # type: ignore
    icon = "group"  # type: ignore
    panels = [
        FieldPanel("name"),
        FieldPanel("website"),
        FieldPanel("featured"),
        FieldPanel("logo"),
    ]


register_snippet(ClientViewSet)
