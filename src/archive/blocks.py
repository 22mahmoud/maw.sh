from django.utils.html import strip_tags
from django.utils.text import Truncator
from wagtail import blocks
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtailmedia.blocks import VideoChooserBlock

from src.base.blocks import CodeBlock
from src.base.blocks.text import HeadingBlock


class VideoStreamBlock(blocks.StreamBlock):
    video_embed = EmbedBlock(
        label="Video URL (YouTube, Vimeo, etc.)",
        help_text="Paste a direct link to your video from YouTube, Vimeo, or other platforms",
    )

    video = VideoChooserBlock(
        help_text="Upload and select a video file from your media library"
    )

    class Meta:  # type: ignore
        label = "Video"


class MediaStreamBlock(VideoStreamBlock):
    image = ImageChooserBlock(
        help_text="Choose an image from your media library to display alongside content"
    )

    class Meta:  # type: ignore
        label = "Media"


class NoteBlockValue(blocks.StructValue):
    @property
    def content_data(self):
        content = self.get("content")
        char_limit = 200

        if not content:
            return {}

        plain_text = strip_tags(content)
        is_truncated = len(plain_text) > char_limit

        truncator = Truncator(content)
        truncated_html = truncator.chars(char_limit, html=True)

        return {
            "truncated": truncated_html,
            "full": content,
            "is_truncated": is_truncated,
        }


class NoteBlock(blocks.StructBlock):
    content = blocks.RichTextBlock(
        features=["bold", "italic", "link", "blockquote", "hr"],
        required=True,
        help_text="Write your note content. Supports rich text formatting like bold, italic, and links",
    )
    media = MediaStreamBlock(
        required=False,
        help_text="Optional: Add images or videos to accompany your note",
    )

    def get_template(self, _, context=None):  # type: ignore
        is_preview = context.get("is_preview", False)  # type: ignore
        if is_preview:
            return "posts/blocks/note_preview.html"
        else:
            return "posts/blocks/note.html"

    class Meta:  # type: ignore
        icon = "doc-full"
        label = "Note"
        value_class = NoteBlockValue


class ArticleBlock(blocks.StructBlock):
    summary = blocks.TextBlock()

    featured_image = ImageChooserBlock(
        help_text="Choose an image from your media library to display alongside content"
    )

    body = blocks.StreamBlock(
        [
            (
                "rich_text",
                blocks.RichTextBlock(
                    features=["bold", "italic", "link", "code"],
                    help_text="Write your article content. Use headings (H2, H3) to structure your text",
                ),
            ),
            (
                "image",
                ImageChooserBlock(
                    help_text="Choose an image from your media library to display alongside content"
                ),
            ),
            (
                "codeblock",
                CodeBlock(),
            ),
            ("heading", HeadingBlock()),
        ]
    )

    def get_template(self, _, context=None):  # type: ignore
        is_preview = context.get("is_preview", False)  # type: ignore
        if is_preview:
            return "posts/blocks/article_preview.html"
        else:
            return "posts/blocks/article.html"

    class Meta:  # type: ignore
        icon = "doc-full"
        label = "Article"


class PhotoBlock(blocks.StructBlock):
    images = blocks.ListBlock(
        ImageChooserBlock(),
        min_num=1,
        label="Photo(s)",
        help_text="Add one or more photos. Click '+ Add Photo' to include multiple images",
    )
    caption = blocks.RichTextBlock(
        features=["bold", "italic", "link"],
        required=False,
        help_text="Optional: Add a caption or description for your photo(s)",
    )

    class Meta:  # type: ignore
        icon = "image"
        label = "Photo"
        template = "posts/blocks/photo.html"


class VideoBlock(blocks.StructBlock):
    videos = VideoStreamBlock(
        required=True,
        label="Video(s)",
        help_text="Add videos either by URL (YouTube/Vimeo) or upload from your media library",
    )
    caption = blocks.RichTextBlock(
        features=["bold", "italic", "link"],
        required=False,
        help_text="Optional: Add a caption or description for your video(s)",
    )

    class Meta:  # type: ignore
        icon = "media"
        label = "Video"
        template = "posts/blocks/video.html"


class ReplyBlock(blocks.StructBlock):
    in_reply_to = blocks.URLBlock(
        required=True, help_text="URL of the original post you're replying to"
    )
    reply_title = blocks.CharBlock(
        required=False, help_text="Title of the post you're replying to (for reference)"
    )
    description = blocks.TextBlock(
        required=False, help_text="Optional: Description of the target page content"
    )
    content = blocks.RichTextBlock(
        features=["bold", "italic", "link"],
        required=True,
        help_text="Write your reply. This will be linked to the original post",
    )

    class Meta:  # type: ignore
        icon = "comment"
        label = "Reply"
        template = "posts/blocks/reply.html"


class LikeBlock(blocks.StructBlock):
    like_of = blocks.URLBlock(
        required=True,
        help_text="URL of the content you want to like (supports IndieWeb 'like-of' microformat)",
    )
    title = blocks.CharBlock(
        required=False, help_text="Optional: Title of the content you're liking"
    )
    description = blocks.TextBlock(
        required=False, help_text="Optional: Description of the target page content"
    )

    class Meta:  # type: ignore
        icon = "pick"
        label = "Like"
        template = "posts/blocks/like.html"


class BookmarkBlock(blocks.StructBlock):
    bookmark_of = blocks.URLBlock(
        required=True,
        help_text="URL of the page you want to bookmark for later reference",
    )
    title = blocks.CharBlock(
        required=False, help_text="Optional: Title of the bookmarked content"
    )
    description = blocks.TextBlock(
        required=False, help_text="Optional: Description of the target page content"
    )
    notes = blocks.RichTextBlock(
        features=["bold", "italic", "link"],
        required=False,
        help_text="Optional: Your personal notes about why you're bookmarking this",
    )

    class Meta:  # type: ignore
        icon = "circle-plus"
        label = "Bookmark"
        template = "posts/blocks/bookmark.html"


class RepostBlock(blocks.StructBlock):
    repost_of = blocks.URLBlock(
        required=True,
        help_text="URL of the original content you want to share with your audience",
    )
    title = blocks.CharBlock(
        required=False, help_text="Optional: Title of the content you're reposting"
    )
    description = blocks.TextBlock(
        required=False, help_text="Optional: Description of the target page content"
    )

    class Meta:  # type: ignore
        icon = "redirect"
        label = "Repost"
        template = "posts/blocks/repost.html"
