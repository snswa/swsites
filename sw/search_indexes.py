import datetime

from haystack import indexes
from haystack import site

from wakawaka.models import WikiPage


class WakawakaWikiPageIndex(indexes.SearchIndex):

    text = indexes.CharField(document=True, use_template=True)
    slug = indexes.CharField(model_attr='slug')
    created = indexes.DateTimeField(model_attr='created')
    modified = indexes.DateTimeField(model_attr='modified')

    def get_queryset(self):
        return WikiPage.objects.all()

site.register(WikiPage, WakawakaWikiPageIndex)
