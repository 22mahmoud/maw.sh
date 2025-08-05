from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlparse

import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from wagtail.images import get_image_model

from src.webmentions.models import Webmention, WebmentionAuthor, WebmentionSync

Image = get_image_model()


class Command(BaseCommand):
    help = "Fetches webmentions from webmention.io and updates the database."

    def add_arguments(self, parser):
        parser.add_argument(
            "--full-resync",
            action="store_true",
            help="Performs a full resync, ignoring the last sync date.",
        )

    def handle(self, *_, **options):
        if not all([settings.WEBMENTION_DOMAIN, settings.WEBMENTION_TOKEN]):
            self.stderr.write(
                self.style.ERROR(
                    "WEBMENTION_DOMAIN and WEBMENTION_TOKEN must be set in Django settings."
                )
            )
            return

        sync_state = WebmentionSync.get_solo()
        since = sync_state.last_sync

        if options["full_resync"]:
            since = None
            self.stdout.write(self.style.WARNING("Performing a full resync."))

        try:
            mentions_data = self._fetch_mentions(since)
        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f"Failed to fetch webmentions: {e}"))
            return

        if not mentions_data:
            self.stdout.write(self.style.SUCCESS("No new webmentions to process."))
            return

        self.stdout.write(f"Found {len(mentions_data)} new webmention(s). Processing...")

        new_mention_count = 0
        with transaction.atomic():
            for mention in mentions_data:
                if self._process_mention(mention):
                    new_mention_count += 1

            sync_state.last_sync = datetime.now(UTC)
            sync_state.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully processed and saved {new_mention_count} new webmention(s)."
            )
        )

    def _fetch_mentions(self, since=None):
        """Builds the URL and fetches data from the webmention.io API."""
        base_url = "https://webmention.io/api/mentions.jf2"
        params = {
            "domain": settings.WEBMENTION_DOMAIN,
            "token": settings.WEBMENTION_TOKEN,
            "per-page": 999,
        }
        if since:
            params["since"] = since.isoformat()

        self.stdout.write(f"Fetching from {base_url} with params: {params.get('since', 'None')}")

        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json().get("children", [])

    def _process_mention(self, mention_data: dict) -> bool:
        wm_id = mention_data.get("wm-id")

        if not wm_id:
            self.stdout.write(self.style.WARNING("Skipping mention with no wm-id."))
            return False

        if Webmention.objects.filter(wm_id=wm_id).exists():
            self.stdout.write(self.style.WARNING(f"Skipping already processed wm-id: {wm_id}"))
            return False

        author_data = mention_data.get("author")
        if not author_data or not author_data.get("url"):
            self.stdout.write(self.style.WARNING(f"Skipping mention {wm_id} with no author URL."))
            return False

        try:
            author = self._get_or_create_author(author_data)
            webmention_instance = Webmention.create_from_api_data(mention_data, author)
            webmention_instance.save()

            self.stdout.write(
                f"  + Saved {webmention_instance.get_type}Webmention for wm-id: {wm_id}"
            )

            return True

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error saving wm-id {wm_id}: {e}"))
            return False

    def _get_or_create_author(self, author_data: dict) -> WebmentionAuthor:
        author_url = author_data.get("url")
        author, _ = WebmentionAuthor.objects.get_or_create(
            url=author_url, defaults={"name": author_data.get("name", "")}
        )

        photo_url = author_data.get("photo")
        if photo_url and not author.photo:
            try:
                response = requests.get(photo_url, timeout=10)
                response.raise_for_status()

                filename = (
                    Path(urlparse(photo_url).path).name or f"{author.id}_avatar.jpg"  # type: ignore
                )

                wagtail_image = Image(
                    title=f"Avatar for {author.name or author.url}",
                    file=ContentFile(response.content, name=filename),
                )

                wagtail_image.save()
                author.photo = wagtail_image  # type: ignore
                author.save(update_fields=["photo"])
                self.stdout.write(f"    - Fetched and saved avatar for {author.name}")

            except requests.exceptions.RequestException as e:
                self.stdout.write(
                    self.style.WARNING(f"Could not fetch author photo from {photo_url}: {e}")
                )
            except Exception as e:
                self.stderr.write(
                    self.style.ERROR(f"Error creating Wagtail Image for {photo_url}: {e}")
                )

        return author
