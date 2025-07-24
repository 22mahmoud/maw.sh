from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.db import transaction

from src.posts.models import BasePostPage


class Command(BaseCommand):
    help = (
        "Creates redirects from the 'legacy_url_path' of pages to their new canonical Wagtail URL."
    )

    def handle(self, *args, **options):
        try:
            current_site = Site.objects.get_current()
        except Site.DoesNotExist:
            self.stderr.write(self.style.ERROR("Current site not found. Please set SITE_ID."))
            return

        self.stdout.write(f"Processing redirects for site: {current_site.name}")

        # Get all concrete models that inherit from BasePostPage
        page_models = BasePostPage.__subclasses__()
        created_count = 0
        updated_count = 0

        # Use a transaction to make the whole process faster
        with transaction.atomic():
            for model in page_models:
                self.stdout.write(f"  - Checking model: {model.__name__}")
                # Use .iterator() for memory efficiency on very large sites
                pages_with_legacy_urls = (
                    model.objects.filter(legacy_url_path__isnull=False)
                    .exclude(legacy_url_path__exact="")
                    .iterator()
                )

                for page in pages_with_legacy_urls:
                    old_path = page.legacy_url_path
                    new_path = page.get_url()

                    if not old_path or not new_path:
                        continue

                    _, created = Redirect.objects.update_or_create(
                        site=current_site,
                        old_path=old_path,
                        defaults={"new_path": new_path},
                    )

                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone! Created {created_count} new redirects. "
                f"Updated {updated_count} existing redirects."
            )
        )
