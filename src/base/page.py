from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
from wagtailseo.models import SeoMixin

from src.base.tags import PageTag


def _resolve_steps(obj, steps):
    current = obj
    for step in steps:
        if isinstance(step, int):
            current = current[step]
            if hasattr(current, "value"):
                current = current.value
        elif hasattr(current, step):
            current = getattr(current, step)
        elif isinstance(current, dict) and step in current:
            current = current[step]
        else:
            raise AttributeError(f"{current} has no step {step}")
    return current


class BasePage(SeoMixin, Page):
    tags = ClusterTaggableManager(through=PageTag, blank=True)

    @property
    def seo_description(self):
        for steps in self.seo_description_sources:
            try:
                value = _resolve_steps(self, steps)
                if value:
                    return str(value)
            except (AttributeError, IndexError, KeyError, TypeError):
                continue

        return (
            "Mahmoud Ashraf — Frontend Engineer from Alexandria, Egypt. "
            "I craft fast, accessible, and user-focused web experiences."
        )

    @property
    def keywords_content(self) -> str:
        if not self.tags.exists():  # type: ignore
            return "indieweb,front-end,linux,personal,blog"

        tag_names = [tag.name for tag in self.tags.all()]  # type: ignore
        return ",".join(tag_names)

    def get_context(self, request):
        from src.base.models import Webring

        context = super().get_context(request)
        context["webrings"] = Webring.objects.all()
        return context

    content_panels = Page.content_panels + [FieldPanel("tags")]

    promote_panels = SeoMixin.seo_panels

    class Meta:  # type: ignore
        abstract = True
