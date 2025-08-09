from django.urls import path

from .feeds import LatestBlogsFeed, LatestFeed

urlpatterns = [
    path("blog/", LatestBlogsFeed()),
    path("feed/", LatestFeed()),
]
