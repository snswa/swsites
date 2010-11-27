from django.conf.urls.defaults import *


urlpatterns = patterns(
    'sw.views',
    (r'^deploy_tests/report_ok$', 'report_ok_view'),
)
