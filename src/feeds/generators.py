from bs4 import BeautifulSoup
from django.utils import feedgenerator


def strip_svg(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for svg in soup.find_all("svg"):
        svg.decompose()
    return str(soup)


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
            handler.addQuickElement("content", strip_svg(content), {"type": "html"})  # type: ignore

        for author in item.get("_authors", []):
            handler.startElement("author", {})  # type:ignore
            handler.addQuickElement("name", author["name"])  # type: ignore
            if author.get("email"):
                handler.addQuickElement("email", author["email"])  # type: ignore
            if author.get("uri"):
                handler.addQuickElement("uri", author["uri"])  # type: ignore
            handler.endElement("author")
