class FeedMixin:
    def _item_categories(self, item):
        return [
            {
                "term": tag.name,
                "scheme": tag.url,
                "label": tag.slug.replace("-", " ").title(),
            }
            for tag in item.get_tags
        ]

    def item_authors(self, item):
        return [
            {
                "name": person.full_name,
                "uri": person.website or person.get_absolute_url(),
                "email": getattr(person, "email", None),
            }
            for person in item.authors()
        ]

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return item.get_absolute_url()

    def item_guid(self, item):
        return self.item_link(item)

    def item_pubdate(self, item):
        return item.first_published_at

    def item_updateddate(self, item):
        return getattr(item, "latest_revision_created_at", item.first_published_at)

    def item_extra_kwargs(self, item):
        return {
            "content": str(item.body),
            "_categories": self._item_categories(item),
        }
