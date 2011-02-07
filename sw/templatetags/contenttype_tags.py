from django.contrib.contenttypes.models import ContentType
from django.template import Library


register = Library()


@register.filter
def contenttypecssname(obj):
    ct = ContentType.objects.get_for_model(obj)
    return u'{0}-{1}'.format(ct.app_label, ct.model)


@register.filter
def contenttype(obj):
    ct = ContentType.objects.get_for_model(obj)
    return u'{0}.{1}'.format(ct.app_label, ct.model)
