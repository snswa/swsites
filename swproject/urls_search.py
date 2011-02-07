from django.conf.urls.defaults import patterns, url

from sw.views import haystack_search


urlpatterns = patterns('',
    url(r'^$', haystack_search, name='haystack_search'),
)
