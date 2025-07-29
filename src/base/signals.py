from contextlib import suppress

from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db.models.signals import post_save
from django.dispatch import receiver
from wagtailmenus.models.menus import MainMenu


@receiver(post_save, sender=MainMenu)
def post_save_menu_page(sender, instance, created, **kwargs):
    for is_authenticated in ("True", "False"):
        cache_key = make_template_fragment_key("main_menu", [is_authenticated])

        with suppress(Exception):
            cache.delete(cache_key)

        print("Saved and cache cleared:", cache_key)
