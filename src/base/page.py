from wagtail.models import Page
from wagtailseo.models import SeoMixin


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

    class Meta:  # type: ignore
        abstract = True
