from wagtail import blocks


class HeadingBlock(blocks.StructBlock):
    heading_text = blocks.RichTextBlock(
        features=["bold", "italic", "link", "code"], required=True
    )
    size = blocks.ChoiceBlock(
        choices=[
            ("", "Select a heading size"),
            ("h1", "H1"),
            ("h2", "H2"),
            ("h3", "H3"),
            ("h4", "H4"),
            ("h5", "H5"),
            ("h6", "H6"),
        ],
        blank=True,
        required=False,
    )

    class Meta:  # type: ignore
        icon = "title"
        template = "blocks/heading_block.html"
