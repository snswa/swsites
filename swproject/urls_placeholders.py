from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('sw.views',
    url(r'^(?P<slug>[\w\._-]+)/$', 'placeholder', name='sw_placeholder'),
)
