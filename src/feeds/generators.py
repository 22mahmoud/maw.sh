from django.utils import feedgenerator


class ExtendedAtomFeed(feedgenerator.Atom1Feed):
    def add_item_elements(self, handler, item):
        super().add_item_elements(handler, item)

        for cat in item.get("_categories", []):
            attrs = {"term": cat["term"]}
            if "scheme" in cat:
                attrs["scheme"] = cat["scheme"]
            if "label" in cat:
                attrs["label"] = cat["label"]
            handler.addQuickElement("category", None, attrs)  # type: ignore

        if content := item.get("content"):
            handler.addQuickElement("content", content, {"type": "html"})  # type: ignore
