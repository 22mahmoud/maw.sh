from wagtail.admin.panels import FieldPanel
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.snippets.models import register_snippet

from .models import Client


class ClientViewSet(SnippetViewSet):
    model = Client
    panels = [
        FieldPanel("name"),
        FieldPanel("website"),
        FieldPanel("featured"),
        FieldPanel("logo"),
    ]


register_snippet(ClientViewSet)
