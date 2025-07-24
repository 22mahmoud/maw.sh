from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from src.base.blocks import CodeBlock


class ListItemStreamBlock(blocks.StreamBlock):
    text = blocks.RichTextBlock(features=["bold", "italic", "link", "code"])
    code = CodeBlock()
    image = ImageChooserBlock()


class ListItemBlock(blocks.StructBlock):
    def __init__(self, local_blocks=(), max_depth=3, _depth=0, *args, **kwargs):
        _depth += 1
        if _depth <= max_depth:
            streamblocks = list(ListItemStreamBlock().child_blocks.items())
            if _depth < max_depth:
                streamblocks += (
                    (
                        "nested_list",
                        ListBlock(local_blocks, max_depth, _depth, *args, **kwargs),
                    ),
                )
            local_blocks += (
                ("content", blocks.StreamBlock(streamblocks, use_json_field=True)),
                *local_blocks,
            )

        super().__init__(local_blocks, _depth=_depth, *args, **kwargs)

    class Meta:  # type: ignore
        icon = "list-ul"
        template = "blocks/list_item_block.html"
        label = "List item"


class ListBlock(blocks.StructBlock):
    def __init__(self, local_blocks=(), max_depth=3, _depth=0, *args, **kwargs):
        local_blocks += (
            (
                "list_type",
                blocks.ChoiceBlock(
                    choices=[("ul", "Unordered"), ("ol", "Ordered")],
                    default="ul",
                    label="List style",
                ),
            ),
            (
                "items",
                blocks.ListBlock(ListItemBlock(max_depth=max_depth, _depth=_depth), label="Items"),
            ),
            *local_blocks,
        )
        super().__init__(local_blocks, _depth=_depth, *args, **kwargs)

    class Meta:  # type: ignore
        icon = "list-ol"
        template = "blocks/list_block.html"
        label = "List"
