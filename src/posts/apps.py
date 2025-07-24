from contextlib import suppress

from django.apps import AppConfig


class PostsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.posts"

    def ready(self):
        with suppress(ImportError):
            import src.posts.signals  # noqa: F401
