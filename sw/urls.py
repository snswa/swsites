from django.conf.urls.defaults import patterns, url


urlpatterns = patterns(
    'sw.views',
    url(r'^deploy_tests/report_ok$', 'report_ok_view'),
    url(r'^temp_move_wiki_page$', 'temp_move_wiki_page', name='temp_move_wiki_page'),
)
