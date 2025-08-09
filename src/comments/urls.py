from django.urls import include, path, re_path

import src.comments.views as views

urlpatterns = [
    re_path(r"^like/(\d+)/$", views.like, name="comments-xtd-like"),
    re_path(r"^dislike/(\d+)/$", views.dislike, name="comments-xtd-dislike"),
    re_path(r"^flag/(\d+)/$", views.flag, name="comments-flag"),
    path("", include("django_comments_xtd.urls")),
]
