from config.env import env
from config.settings.wagtail_prod import *  # noqa: E402, F403

from .base import *  # noqa: F403
from .base import BASE_DIR, MIDDLEWARE

MIDDLEWARE.append("whitenoise.middleware.WhiteNoiseMiddleware")

STORAGES = {
    "default": {
        "BACKEND": "config.settings.django_storage.MediaR2Storage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    "wagtailrenditions": {
        "BACKEND": "config.settings.django_storage.WagtailRenditionStorage",
    },
}

STATICFILES_DIRS = [BASE_DIR / "static"]

DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

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


def whitenoise_headers(headers, path, url):
    headers["accept-encoding"] = "gzip, deflate, br"


WHITENOISE_ADD_HEADERS_FUNCTION = whitenoise_headers
