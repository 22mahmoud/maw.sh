from contextlib import suppress

from django.apps import AppConfig


class ClientsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.clients"

    def ready(self) -> None:
        with suppress(ImportError):
            import src.clients.signals  # noqa: F401
