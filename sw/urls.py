from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('',
    url(r'^deploy_tests/report_ok$', 'sw.views.report_ok_view'),
)
