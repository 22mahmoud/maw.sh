# pyright: reportAssignmentType=false
# pyright: reportAttributeAccessIssue=false
# pyright: reportOperatorIssue=false
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import Guestbook


class GuestbookSubmissionViewSet(SnippetViewSet):
    model = Guestbook
    menu_label = "Guestbook Submissions"
    icon = "comment"
    add_to_admin_menu = True
    menu_order = 400
    list_display = ("name", "emoji", "message", "url")
    list_filter = ("created_at",)
    search_fields = ("name", "url", "message")
    panels = [
        FieldPanel("name", read_only=True),
        FieldPanel("emoji", read_only=True),
        FieldPanel("message", read_only=False),
        FieldPanel("url", read_only=False),
        FieldPanel("visibility"),
        FieldPanel("style", read_only=True),
        FieldPanel("radius", read_only=True),
        FieldPanel("created_at", read_only=True),
    ]


register_snippet(GuestbookSubmissionViewSet)
