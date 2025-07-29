from contextlib import suppress

from django.apps import AppConfig


class BaseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.base"

    def ready(self):
        with suppress(ImportError):
            import src.base.signals  # noqa: F401
