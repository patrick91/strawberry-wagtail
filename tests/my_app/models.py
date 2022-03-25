from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page


class BlogPage(Page):
    body = RichTextField()


class CMSPage(Page):
    body = StreamField(
        [
            ("heading", blocks.CharBlock(form_classname="full title")),
            ("paragraph", blocks.RichTextBlock()),
            (
                "two_columns",
                blocks.StreamBlock(
                    [
                        ("text", blocks.RichTextBlock()),
                    ],
                    min_num=2,
                    max_num=2,
                ),
            ),
        ]
    )
