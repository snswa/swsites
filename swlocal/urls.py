from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('swlocal.views',
    url(r'^$', 'index', name='swlocal_index'),
)