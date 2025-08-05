from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.images.models import AbstractImage, AbstractRendition, Image


class CustomImage(AbstractImage):
    caption = models.CharField(max_length=255, blank=True)

    admin_form_fields = Image.admin_form_fields + ("caption",)

    class Meta(AbstractImage.Meta):
        verbose_name = _("image")
        verbose_name_plural = _("images")
        permissions = [
            ("choose_image", "Can choose image"),
        ]


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(CustomImage, on_delete=models.CASCADE, related_name="renditions")

    class Meta:  # type: ignore
        unique_together = (("image", "filter_spec", "focal_point_key"),)
