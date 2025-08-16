import contextlib
from datetime import datetime

import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from django.utils.text import slugify
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.images import get_image_model

from src.base.page import BasePage

Image = get_image_model()


class WatchListIndexPage(BasePage):
    subpage_types = ["WatchItemPage"]

    def get_items(self):
        return WatchItemPage.objects.child_of(self).live().order_by("-watch_date")  # type: ignore


class WatchItemPage(BasePage):
    WATCH_STATUS = [
        ("watching", "Currently Watching"),
        ("completed", "Completed"),
        ("planned", "Plan to Watch"),
        ("abandoned", "Abandoned / Dropped"),
    ]

    WATCH_TYPE = [
        ("movie", "Movie"),
        ("tv", "TV Show"),
    ]

    tmdb_id = models.PositiveIntegerField(blank=True, null=True, help_text="TMDb ID for Movie/TV")
    watch_type = models.CharField(max_length=20, choices=WATCH_TYPE, default="movie")
    watch_status = models.CharField(max_length=20, choices=WATCH_STATUS, default="watching")
    watch_date = models.DateField(blank=True, null=True)

    overview = models.TextField(blank=True)
    release_date = models.DateField(blank=True, null=True)
    poster_image = models.ForeignKey(
        "images.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content = RichTextField(  # type: ignore
        features=["bold", "italic", "link", "blockquote", "code", "ul", "ol", "hr"],
        blank=True,
        help_text=(
            "Write your note content. Supports rich text formatting like bold, italic, and links"
        ),
    )

    content_panels = BasePage.content_panels + [
        FieldPanel("tmdb_id"),
        FieldPanel("watch_type"),
        FieldPanel("watch_status"),
        FieldPanel("watch_date"),
        FieldPanel("overview"),
        FieldPanel("release_date"),
        FieldPanel("poster_image"),
        FieldPanel("content"),
    ]

    def save_revision(self, *args, **kwargs):
        """
        On save, if TMDb ID is set, fetch and store metadata + poster image.
        """
        if self.tmdb_id:
            try:
                tmdb_api_key = settings.TMDB_API_KEY
                if self.watch_type == "movie":
                    url = f"https://api.themoviedb.org/3/movie/{self.tmdb_id}?api_key={tmdb_api_key}&language=en-US"
                    keywords_url = f"https://api.themoviedb.org/3/movie/{self.tmdb_id}/keywords?api_key={tmdb_api_key}"
                elif self.watch_type == "tv":
                    url = f"https://api.themoviedb.org/3/tv/{self.tmdb_id}?api_key={tmdb_api_key}&language=en-US"
                    keywords_url = f"https://api.themoviedb.org/3/tv/{self.tmdb_id}/keywords?api_key={tmdb_api_key}"
                else:
                    url = None
                    keywords_url = None

                if url:
                    r = requests.get(url)
                    if r.status_code == 200:
                        data = r.json()
                        title = data.get("title") or data.get("name")
                        if not self.title and title:
                            self.title = title
                        if not self.overview and data.get("overview"):
                            self.overview = data["overview"]
                        if title and not self.slug:
                            self.slug = slugify(title)

                        date_field = data.get("release_date") or data.get("first_air_date")
                        if not self.release_date and date_field:
                            with contextlib.suppress(ValueError):
                                self.release_date = datetime.strptime(date_field, "%Y-%m-%d").date()

                        if not self.poster_image and data.get("poster_path"):
                            poster_url = f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
                            img_response = requests.get(poster_url)
                            if img_response.status_code == 200:
                                image_file = ContentFile(
                                    img_response.content, name=f"{slugify(title)}_poster.jpg"
                                )
                                image_instance = Image(
                                    title=f"{title} Poster",
                                    file=image_file,
                                )
                                image_instance.save()
                                self.poster_image = image_instance

                        if keywords_url:
                            kr = requests.get(keywords_url)
                            if kr.status_code == 200:
                                keywords_data = kr.json()
                                keywords_list = []
                                if self.watch_type == "movie":
                                    keywords_list = [
                                        kw["name"] for kw in keywords_data.get("keywords", [])
                                    ]
                                elif self.watch_type == "tv":
                                    keywords_list = [
                                        kw["name"] for kw in keywords_data.get("results", [])
                                    ]

                                if keywords_list:
                                    self.tags.add(*keywords_list)
            except Exception as e:
                print(f"TMDb fetch failed: {e}")

        return super().save_revision(*args, **kwargs)
