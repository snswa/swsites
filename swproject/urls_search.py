from django.conf.urls.defaults import patterns, url

from haystack.forms import SearchForm
from haystack.views import SearchView


search_view = SearchView(
    form_class=SearchForm,
)


urlpatterns = patterns('haystack.views',
    url(r'^$', search_view, name='haystack_search'),
)
