from contextlib import suppress

from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.projects"

    def ready(self) -> None:
        with suppress(ImportError):
            import src.projects.signals  # noqa: F401
