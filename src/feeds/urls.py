from django.urls import path

from .feeds import LatestBLogsFeed, LatestFeed

urlpatterns = [
    path("blog/", LatestBLogsFeed()),
    path("feed/", LatestFeed()),
]
