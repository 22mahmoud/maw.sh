from wagtail import blocks


class FeaturedProjectsStaticBlock(blocks.StaticBlock):
    def get_context(self, value, parent_context=None):
        from .models import ProjectPage

        context = super().get_context(value, parent_context=parent_context)

        featured_projects = (
            ProjectPage.objects.live()  # type: ignore
            .public()
            .filter(is_featured=True)
            .order_by("-first_published_at")
        )

        context["projects"] = [p.specific for p in featured_projects]

        return context

    class Meta:  # type: ignore
        icon = "form"
        label = "Featured Projects"
        template = "blocks/featured_projects_block.html"
