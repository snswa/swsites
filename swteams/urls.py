from django.conf.urls.defaults import *

import swtopics.views


urlpatterns = patterns('',
    url(name=   'team_activity_history',
        regex=  r'^teams/(?P<slug>[\w\._-]+)/activity/$',
        view=   'swteams.views.activity',
    ),
    #
    url(name=   'team_topics',
        regex=  r'^teams/(?P<slug>[\w\._-]+)/topics/$',
        view=   'swteams.views.topics_with_team_slug',
        kwargs= dict(
            queryset_fn=swtopics.views.team_topics_queryset_fn,
        ),
    ),
    url(name=   'team_topic_create',
        regex=  r'^teams/(?P<slug>[\w\._-]+)/topics/create/$',
        view=   'iris.views.topic_create',
        kwargs= dict(
            post_topic_create=swtopics.views.team_post_topic_create,
        ),
    ),
    #
    url(name=   'team_event_topics',
        regex=  r'^teams/(?P<slug>[\w\._-]+)/events/(?P<event_id>\d+)/topics/$',
        view=   'swteams.views.topics_with_team_slug',
        kwargs= dict(
            queryset_fn=swtopics.views.team_event_topics_queryset_fn,
        ),
    ),
    url(name=   'team_event_topic_create',
        regex=  r'^teams/(?P<slug>[\w\._-]+)/events/(?P<event_id>\d+)/topics/create/$',
        view=   'iris.views.topic_create',
        kwargs= dict(
            post_topic_create=swtopics.views.team_event_post_topic_create,
        ),
    ),
)
