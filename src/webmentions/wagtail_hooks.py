# pyright: reportAssignmentType=false
# pyright: reportAttributeAccessIssue=false
# pyright: reportOperatorIssue=false
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from .models import (
    BookmarkWebmention,
    LikeWebmention,
    MentionWebmention,
    ReplyWebmention,
    RepostWebmention,
    RSVPWebmention,
    WebmentionAuthor,
)


class WebmentionAuthorViewSet(SnippetViewSet):
    model = WebmentionAuthor
    menu_label = "Authors"
    icon = "user"
    list_display = ("name", "url", "photo_preview")
    search_fields = ("name", "url")


class BaseWebmentionViewSet(SnippetViewSet):
    list_display = ("author", "wm_target", "wm_received")
    list_per_page = 25
    search_fields = ("wm_source", "wm_target", "author__name")
    list_filter = ["author"]

    def get_queryset(self, request):
        return self.model.objects.all()


class LikeWebmentionViewSet(BaseWebmentionViewSet):
    model = LikeWebmention
    menu_label = "Likes"
    icon = "pick"
    list_display = BaseWebmentionViewSet.list_display + ("like_of",)
    search_fields = BaseWebmentionViewSet.search_fields + ("like_of",)


class ReplyWebmentionViewSet(BaseWebmentionViewSet):
    model = ReplyWebmention
    menu_label = "Replies"
    icon = "comment"
    list_display = BaseWebmentionViewSet.list_display + ("content_text",)
    search_fields = BaseWebmentionViewSet.search_fields + ("content_text",)


class RepostWebmentionViewSet(BaseWebmentionViewSet):
    model = RepostWebmention
    menu_label = "Reposts"
    icon = "redirect"
    list_display = BaseWebmentionViewSet.list_display + ("repost_of",)
    search_fields = BaseWebmentionViewSet.search_fields + ("repost_of",)


class BookmarkWebmentionViewSet(BaseWebmentionViewSet):
    model = BookmarkWebmention
    menu_label = "Bookmarks"
    icon = "circle-plus"
    list_display = BaseWebmentionViewSet.list_display + ("bookmark_of",)
    search_fields = BaseWebmentionViewSet.search_fields + ("bookmark_of",)


class MentionWebmentionViewSet(BaseWebmentionViewSet):
    model = MentionWebmention
    menu_label = "Mentions"
    icon = "tag"
    list_display = BaseWebmentionViewSet.list_display + ("mention_of",)
    search_fields = BaseWebmentionViewSet.search_fields + ("mention_of",)


class RSVPWebmentionViewSet(BaseWebmentionViewSet):
    model = RSVPWebmention
    menu_label = "RSVPs"
    icon = "date"
    list_display = BaseWebmentionViewSet.list_display + ("rsvp",)
    search_fields = BaseWebmentionViewSet.search_fields


class WebmentionGroup(SnippetViewSetGroup):
    menu_label = "Webmentions"
    menu_icon = "comment"
    menu_order = 200
    items = (
        ReplyWebmentionViewSet,
        LikeWebmentionViewSet,
        RepostWebmentionViewSet,
        BookmarkWebmentionViewSet,
        MentionWebmentionViewSet,
        RSVPWebmentionViewSet,
        WebmentionAuthorViewSet,
    )


register_snippet(WebmentionGroup)
