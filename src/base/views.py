from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_GET

from src.base.models import DummyPage

robots_txt_content = """\
User-agent: *
Sitemap: https://site.mahmoudashraf.dev/sitemap.xml
"""


@require_GET
def robots_txt(_):
    return HttpResponse(robots_txt_content, content_type="text/plain")


def error_404_view(request, exception=None):
    page = DummyPage(
        title=_("Page not found"),
        seo_title=_("404 – Page not found"),
    )

    return render(request, "404.html", {"page": page}, status=404)


def error_500_view(request, exception=None):
    return render(request, "500.html", status=500)
