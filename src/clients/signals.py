from contextlib import suppress

from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db.models.signals import post_save
from django.dispatch import receiver

from src.clients.models import Client


@receiver(post_save, sender=Client)
def post_save_menu_page(sender, instance, created, **kwargs):
    cache_key = make_template_fragment_key("clients_marquee")

    with suppress(Exception):
        cache.delete(cache_key)

    print("Saved and cache cleared:", cache_key)
