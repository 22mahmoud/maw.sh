from django.db import models
from wagtail.models import Page


class DummySearchPage(Page):
    introduction = models.TextField()
    search_fields = ()
