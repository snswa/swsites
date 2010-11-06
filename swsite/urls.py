from django.conf.urls.defaults import *


urlpatterns = patterns(
    'swsite.views',
    (r'^deploy_tests/report_ok$', 'report_ok_view'),
)
