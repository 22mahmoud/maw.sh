from contextlib import suppress

from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db.models.signals import post_save
from django.dispatch import receiver

from src.projects.models import ProjectPage


@receiver(post_save, sender=ProjectPage)
def post_save_menu_page(sender, instance, created, **kwargs):
    cache_key = make_template_fragment_key("featured_projects")

    with suppress(Exception):
        cache.delete(cache_key)

    print("Saved and cache cleared:", cache_key)
