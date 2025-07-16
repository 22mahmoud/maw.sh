# pyright: reportAssignmentType=false
# pyright: reportAttributeAccessIssue=false
# pyright: reportOperatorIssue=false
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import ContactSubmission


class ContactSubmissionViewSet(SnippetViewSet):
    model = ContactSubmission
    menu_label = "Contact Submissions"
    icon = "mail"
    add_to_admin_menu = True
    list_display = ("name", "email", "submitted_at")
    list_filter = ("submitted_at",)
    search_fields = ("name", "email", "message")
    panels = [
        FieldPanel("name", read_only=True),
        FieldPanel("email", read_only=True),
        FieldPanel("message", read_only=True),
        FieldPanel("submitted_at", read_only=True),
    ]


register_snippet(ContactSubmissionViewSet)
