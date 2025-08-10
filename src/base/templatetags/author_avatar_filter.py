from django import template

register = template.Library()


@register.filter
def author_link_class(author_count):
    base = "h-card w-8 ht-8 rounded-full first:ml-0 border-2 border-solid border-darker -ml-4"
    if author_count > 1:
        return base + " transform transition-transform duration-200 hover:scale-110 hover:z-10"
    return base
