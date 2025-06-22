WAGTAIL_INSTALLED_APPS = [
    # my apps
    "src.projects",
    "src.clients",
    "src.base",
    "src.seo",
    # wagtail core apps
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.contrib.settings",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.contrib.styleguide",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    # 3rd party apps
    "wagtailmedia",
    "taggit",
    "modelcluster",
]

WAGTAIL_MIDDLEWARE = [
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

WAGTAIL_TEMPLATE_CONTEXT_PROCESSORS = [
    "wagtail.contrib.settings.context_processors.settings"
]

WAGTAIL_SITE_NAME = "Mahmoud Ashraf"
WAGTAILADMIN_BASE_URL = "http:localhost:8000"

# Replace the search backend
# WAGTAILSEARCH_BACKENDS = {
#  'default': {
#    'BACKEND': 'wagtail.search.backends.elasticsearch8',
#    'INDEX': 'myapp'
#  }
# }

# Wagtail email notifications from address
# WAGTAILADMIN_NOTIFICATION_FROM_EMAIL = 'wagtail@myhost.io'

# Wagtail email notification format
# WAGTAILADMIN_NOTIFICATION_USE_HTML = True

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
