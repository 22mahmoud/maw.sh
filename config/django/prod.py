from csp.constants import NONCE, NONE, SELF

from config.env import env
from config.settings.wagtail_prod import *  # noqa: E402, F403
from config.settings.whitenoise import *  # noqa: F403

from .base import *  # noqa: F403
from .base import BASE_DIR

STORAGES = {
    "default": {
        "BACKEND": "config.settings.django_storage.MediaR2Storage",
    },
    "staticfiles": {
        "BACKEND": "config.settings.whitenoise.CustomStaticFilesStorage",
    },
    "wagtailrenditions": {
        "BACKEND": "config.settings.django_storage.WagtailRenditionStorage",
    },
}

STATICFILES_DIRS = [BASE_DIR / "static"]

DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = "lax"

DEFAULT_HSTS_SECONDS = 30 * 24 * 60 * 60  # 30 days
SECURE_HSTS_SECONDS = int(env.int("SECURE_HSTS_SECONDS", DEFAULT_HSTS_SECONDS))

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": env.str("DJANGO_LOG_LEVEL", "INFO"),
        },
    },
}

EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"

EMAIL_HOST = env.str("EMAIL_HOST", "")
EMAIL_PORT = env.str("EMAIL_PORT", "")
EMAIL_HOST_USER = env.str("EMAIL_USER", "")
EMAIL_HOST_PASSWORD = env.str("EMAIL_PASSWORD", "")
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = env.str("EMAIL_FROM", "")

CONTENT_SECURITY_POLICY = {
    "EXCLUDE_URL_PREFIXES": ["/admin/", "/cms/"],
    "DIRECTIVES": {
        "default-src": [NONE],
        "script-src": [SELF, NONCE],
        "style-src": [SELF, NONCE],
        "font-src": [SELF],
        "img-src": [
            SELF,
            "data:",
            "https://*.tenor.com",
            "https://*.tenor.com",
            "https://*.imgur.com",
            "https://static.mahmoudashraf.dev",
            "https://www.gravatar.com",
        ],
        "connect-src": [SELF],
        "manifest-src": [SELF],
        "object-src": [NONE],
        "frame-ancestors": [SELF],
        "form-action": [
            SELF,
            "https://github.com",
            "https://accounts.google.com",
        ],
        "base-uri": [SELF],
        "upgrade-insecure-requests": True,
    },
}
