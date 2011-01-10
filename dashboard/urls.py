import datetime

from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('dashboard.views',
    url(name=   'dashboard_index',
        regex=  r'^$',
        view=   'index',
    ),
    url(name=   'dashboard_actions',
        regex=  r'^activity/$',
        view=   'actions',
    ),
    url(name=   'dashboard_topics',
        regex=  r'^topics/$',
        view=   'topics',
    ),
    url(name=   'dashboard_events',
        regex=  r'^events/$',
        view=   'events',
        kwargs= dict(
            weeks=6,
            jump_weeks=4,
            start_date=datetime.date.today,
        ),
    ),
)
