from django.contrib.contenttypes.models import ContentType
from django.template import Library


register = Library()


@register.filter
def searchresulttemplate(obj):
    ct = ContentType.objects.get_for_model(obj)
    return u'search/results/{0}/{1}.html'.format(ct.app_label, ct.model)
