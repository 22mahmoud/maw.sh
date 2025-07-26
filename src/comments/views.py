import django_comments_xtd.views as xtd_views
from django.conf import settings
from django.shortcuts import resolve_url
from django_htmx.http import HttpResponseClientRedirect


def like(request, comment_id, next_url=None, **kwargs):
    if not request.user.is_authenticated and request.htmx:
        login_url = resolve_url(settings.LOGIN_URL)
        return HttpResponseClientRedirect(f"{login_url}?next={request.path}")

    return xtd_views.like(request, comment_id, next_url, **kwargs)


def dislike(request, comment_id, next_url=None, **kwargs):
    if not request.user.is_authenticated and request.htmx:
        login_url = resolve_url(settings.LOGIN_URL)
        return HttpResponseClientRedirect(f"{login_url}?next={request.path}")

    return xtd_views.dislike(request, comment_id, next_url, **kwargs)


def flag(request, comment_id, next_url=None, **kwargs):
    if not request.user.is_authenticated and request.htmx:
        login_url = resolve_url(settings.LOGIN_URL)
        return HttpResponseClientRedirect(f"{login_url}?next={request.path}")

    return xtd_views.flag(request, comment_id, next_url, **kwargs)
