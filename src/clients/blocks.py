from wagtail import blocks

from .models import Client


class ClientsMarqueeStaticBlock(blocks.StaticBlock):
    class Meta:  # type: ignore
        icon = "clipboard-list"
        label = "Clients Marquee"
        template = "blocks/clients_marquee_block.html"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        try:
            context["clients"] = Client.objects.filter(featured=True)
            return context
        except Client.DoesNotExist:
            context["clients"] = []
            return context
