from django.apps import AppConfig


class PostsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.posts"

    def ready(self):
        try:
            import src.posts.signals  # noqa F401
        except ImportError:
            pass
