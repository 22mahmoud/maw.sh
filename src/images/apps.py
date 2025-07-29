from wagtail.images.apps import WagtailImagesAppConfig


class CustomImagesAppConfig(WagtailImagesAppConfig):
    default_attrs = {"decoding": "async", "loading": "lazy"}
