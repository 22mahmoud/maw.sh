from django.http import HttpResponse
from django.views.decorators.http import require_GET

robots_txt_content = """\
User-agent: *
Sitemap: https://site.mahmoudashraf.dev/sitemap.xml
"""


@require_GET
def robots_txt(_):
    return HttpResponse(robots_txt_content, content_type="text/plain")
