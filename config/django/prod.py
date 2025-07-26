from config.env import env
from config.settings.wagtail_prod import *  # noqa: E402, F403
from config.settings.whitenoise import *  # noqa: F403

from .base import *  # noqa: F403
from .base import BASE_DIR, MIDDLEWARE

MIDDLEWARE.append("whitenoise.middleware.WhiteNoiseMiddleware")

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
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

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

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = env.str("EMAIL_HOST", "")
EMAIL_PORT = env.str("EMAIL_PORT", "")
EMAIL_HOST_USER = env.str("EMAIL_USER", "")
EMAIL_HOST_PASSWORD = env.str("EMAIL_PASSWORD", "")
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = env.str("EMAIL_FROM", "")
