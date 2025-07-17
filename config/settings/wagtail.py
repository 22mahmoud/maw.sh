WAGTAIL_INSTALLED_APPS = [
    # my apps
    "src.our_forms",
    "src.webmentions",
    "src.videos",
    "src.photos",
    "src.replies",
    "src.bookmarks",
    "src.reposts",
    "src.likes",
    "src.articles",
    "src.notes",
    "src.posts",
    "src.projects",
    "src.clients",
    "src.home",
    "src.base",
    "src.seo",
    # wagtail core apps
    "wagtail.contrib.frontend_cache",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.settings",
    "wagtail.contrib.styleguide",
    "wagtail.contrib.routable_page",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "src.base.apps.CustomImagesAppConfig",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    # 3rd party apps
    "wagtailmenus",
    "wagtailmedia",
    "taggit",
    "modelcluster",
]

WAGTAIL_MIDDLEWARE = [
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

WAGTAIL_TEMPLATE_CONTEXT_PROCESSORS = [
    "wagtail.contrib.settings.context_processors.settings",
    "wagtailmenus.context_processors.wagtailmenus",
]

WAGTAIL_SITE_NAME = "Mahmoud Ashraf"
WAGTAILADMIN_BASE_URL = "http:localhost:8000"

# Allowed file extensions for documents in the document library.
# This can be omitted to allow all files, but note that this may present a security risk
# if untrusted users are allowed to upload files -
# see https://docs.wagtail.org/en/stable/advanced_topics/deploying.html#user-uploaded-files
WAGTAILDOCS_EXTENSIONS = [
    "csv",
    "docx",
    "key",
    "odt",
    "pdf",
    "pptx",
    "rtf",
    "txt",
    "xlsx",
    "zip",
]

WAGTAILMEDIA = {
    "MEDIA_MODEL": "wagtailmedia.Media",
    "MEDIA_FORM_BASE": "",
    "AUDIO_EXTENSIONS": [
        "aac",
        "aiff",
        "flac",
        "m4a",
        "m4b",
        "mp3",
        "ogg",
        "wav",
    ],
    "VIDEO_EXTENSIONS": [
        "avi",
        "h264",
        "m4v",
        "mkv",
        "mov",
        "mp4",
        "mpeg",
        "mpg",
        "ogv",
        "webm",
    ],
}

# Reverse the default case-sensitive handling of tags
TAGGIT_CASE_INSENSITIVE = True
