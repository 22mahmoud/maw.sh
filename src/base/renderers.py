from django.forms import BoundField
from django.forms.renderers import TemplatesSetting


class CustomBoundField(BoundField):
    def css_classes(self, extra_classes=None):
        meta = getattr(getattr(self.form, "Meta", None), "container_classes", {})
        field_class = meta.get(self.name, "")
        parent_css_classes = super().css_classes(extra_classes)

        if field_class:
            return f"{field_class} {parent_css_classes}".strip()

        return parent_css_classes

    def label_tag(self, contents=None, attrs=None, label_suffix=None, tag=None):
        attrs = attrs or {}
        meta = getattr(getattr(self.form, "Meta", None), "label_classes", {})
        label_class = meta.get(self.name, "")

        if label_class:
            attrs["class"] = label_class

        return super().label_tag(contents, attrs, label_suffix, tag)  # type: ignore


class FormRenderer(TemplatesSetting):
    bound_field_class = CustomBoundField
