from wagtail import blocks


class HeadingBlock(blocks.StructBlock):
    heading_text = blocks.RichTextBlock(features=["bold", "italic", "link", "code"], required=True)

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

    text_position = blocks.ChoiceBlock(
        choices=[
            ("left", "Left"),
            ("center", "Center"),
            ("right", "Right"),
        ],
        default="left",
        required=False,
    )

    text_size = blocks.ChoiceBlock(
        choices=[
            ("text-xs", "Extra Small"),
            ("text-sm", "Small"),
            ("text-base", "Base"),
            ("text-lg", "Large"),
            ("text-xl", "XL"),
            ("text-2xl", "2XL"),
            ("text-3xl", "3XL"),
            ("text-4xl", "4XL"),
            ("text-5xl", "5XL"),
            ("text-6xl", "6XL"),
            ("text-7xl", "7XL"),
            ("text-8xl", "8XL"),
            ("text-9xl", "9XL"),
        ],
        required=False,
        blank=True,
    )

    use_anchor = blocks.BooleanBlock(required=False, default=False)

    class Meta:  # type: ignore
        icon = "title"
        template = "blocks/heading_block.html"
