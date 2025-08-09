from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import BasePostPage


@receiver(post_save)
def create_or_update_legacy_redirect(sender, instance, **kwargs):
    if not isinstance(instance, BasePostPage):
        return

    if instance.legacy_url_path:
        try:
            current_site = Site.objects.get_current()
            new_path = instance.get_url()

            if new_path:  # Ensure the page has a URL
                Redirect.objects.update_or_create(
                    site=current_site,
                    old_path=instance.legacy_url_path,
                    defaults={"new_path": new_path},
                )
        except ObjectDoesNotExist:
            pass
