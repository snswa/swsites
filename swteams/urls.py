from django.conf.urls.defaults import *

from swtopics.views import team_post_topic_create, team_topics_queryset_fn


urlpatterns = patterns('',
    url(name=   'team_activity_history',
        regex=  r'^teams/(?P<slug>[\w\._-]+)/activity/$',
        view=   'swteams.views.activity',
    ),
    url(name=   'team_topics',
        regex=  r'^teams/(?P<slug>[\w\._-]+)/topics/$',
        view=   'swteams.views.topics',
        kwargs= dict(
            queryset_fn=team_topics_queryset_fn,
        ),
    ),
    url(name=   'team_topic_create',
        regex=  r'^teams/(?P<slug>[\w\._-]+)/topics/create/$',
        view=   'iris.views.topic_create',
        kwargs= dict(
            post_topic_create=team_post_topic_create,
        ),
    ),
)
