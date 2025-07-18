from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.fields import StreamField

from src.base.models import PageTag
from src.posts.blocks import NoteBlock
from src.posts.models import BasePostPage, BasePostsIndexPage
from src.posts.utils import get_post_content_panels, get_post_search_fields


class NotesPageIndex(BasePostsIndexPage):
    subpage_types = ["NotesPage"]
    template = "archive/archive_page.html"

    def get_posts_queryset(self):
        return (
            NotesPage.objects.child_of(self)  # type: ignore
            .live()
            .public()
            .order_by("-first_published_at")
        )


class NotesPage(BasePostPage):  # type: ignore
    template = "archive/post_page.html"
    body = StreamField(
        [("note", NoteBlock())],
        blank=False,
        min_num=1,
        max_num=1,
        use_json_field=True,
    )
    tags = ClusterTaggableManager(through=PageTag, blank=True)
    parent_page_types = ["NotesPageIndex"]
    subpage_types = []
    content_panels = get_post_content_panels()
    search_fields = get_post_search_fields()
