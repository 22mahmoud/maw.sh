from django.forms import BoundField
from django.forms.renderers import TemplatesSetting


class CustomBoundField(BoundField):
    def css_classes(self, extra_classes=None):
        container_class = self.field.widget.attrs.pop("container_class", None)
        parent_css_classes = super().css_classes(extra_classes)

        if container_class:
            return f"{container_class} {parent_css_classes}".strip()

        return parent_css_classes


class CustomRenderer(TemplatesSetting):
    bound_field_class = CustomBoundField
