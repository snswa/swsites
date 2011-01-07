from django.template import Library


register = Library()


@register.filter
def qslimit(queryset, limit):
    return queryset[:limit]
