from django_comments_xtd.forms import XtdCommentForm as DjangoXtdCommentForm

from src.base.renderers import FormRenderer


class XtdCommentForm(DjangoXtdCommentForm):
    default_renderer = FormRenderer()
