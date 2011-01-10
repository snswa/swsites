# Top-level URLs

import datetime

import django
from django.conf import settings
from django.conf.urls.defaults import include, patterns, url
from django.contrib import admin
from django.views.generic.simple import redirect_to

if django.VERSION >= (1, 3):
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
else:
    from staticfiles.urls import staticfiles_urlpatterns

from groups.bridge import ContentBridge
from iris.forms import TopicForm
import iris.views
from sw.forms import ProfileForm
from swproject import predicates
from swtopics.views import team_post_topic_create, team_topics_queryset_fn
from teams.models import Team


admin.autodiscover()


# Site-wide error handlers.
handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'


# Begin with empty patterns.
urlpatterns = patterns('')

# Serve static files in debug mode.
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

# Group bridges
team_bridge = ContentBridge(Team)


NEW_VOLUNTEER = {
    'login_required': True,
    'email_preferred': True,
    'profile_preferred': True,
}

VERIFIED_VOLUNTEER = {
    'login_required': True,
    'email_required': True,
    'profile_required': True,
}


urlpatterns += patterns('',
    # Deployment tests and temporary views.
    url(regex=  r'^_site/',
        view=   include('sw.urls'),
    ),
    url(regex=  r'^admin/',
        view=   include(admin.site.urls),
    ),
    url(regex=  r'^admin/doc/',
        view=   include('django.contrib.admindocs.urls'),
    ),
    url(regex=  r'^sentry/',
        view=   include('sentry.urls'),
    ),

    # Figure out how to mesh these two together for login.
    url(regex=  r'^accounts/',
        view=   include('allauth.urls'),
        kwargs= dict(
            email_preferred=True,
            profile_preferred=True,
        ),
    ),
    url(name=   'sw_hq',
        regex=  r'^hq/',
        view=   'sw.views.hq',
    ),

    url(regex=  r'^attachments/',
        view=   include('attachments.urls'),
        kwargs= VERIFIED_VOLUNTEER,
    ),
    url(regex=  r'^comments/',
        view=   include('django.contrib.comments.urls'),
        kwargs= VERIFIED_VOLUNTEER,
    ),
    url(regex=  r'^dashboard/',
        view=   include('dashboard.urls'),
        kwargs= VERIFIED_VOLUNTEER,
    ),
    url(regex=  r'^features/',
        view=   include('featurelabs.urls'),
        kwargs= VERIFIED_VOLUNTEER,
    ),
    url(regex=  r'^local/',
        view=   include('swlocal.urls'),
        kwargs= NEW_VOLUNTEER,
    ),
    url(regex=  r'^placeholder/',
        view=   include('swproject.urls_placeholders'),
        kwargs= VERIFIED_VOLUNTEER,
    ),
    url(regex=  r'^profiles/',
        view=   include('idios.urls'),
        kwargs= dict(
            NEW_VOLUNTEER,
            form_class=ProfileForm,
        ),
    ),
    url(regex=  r'^relationships/',
        view=   include('relationships.urls'),
        kwargs= NEW_VOLUNTEER,
    ),
    url(regex=  r'^search/',
        view=   include('swproject.urls_search'),
        kwargs= VERIFIED_VOLUNTEER,
    ),
    url(r'^topics/', include('iris.urls'), kwargs=NEW_VOLUNTEER),
    url(r'^voting/', include('voting.urls'), kwargs=VERIFIED_VOLUNTEER),
)


# Team URLs.
def team_topics(*args, **kwargs):
    # Insert the group into team_topics
    # @@@ get this abstracted?
    slug = kwargs['slug']
    extra_context = kwargs.setdefault('extra_context', {})
    extra_context['group'] = Team.objects.get(slug=slug)
    return iris.views.topics(*args, **kwargs)
urlpatterns += patterns('',
    url(name=   'team_activity_history',
        regex=  r'^teams/(?P<slug>[\w\._-]+)/activity/$',
        view=   'sw.views.team_activity_history',
        kwargs= VERIFIED_VOLUNTEER,
    ),
    url(name=   'team_topics',
        regex=  r'^teams/(?P<slug>[\w\._-]+)/topics/$',
        view=   team_topics,
        kwargs= dict(
            VERIFIED_VOLUNTEER,
            queryset_fn=team_topics_queryset_fn,
        ),
    ),
    url(name=   'team_topic_create',
        regex=  r'^teams/(?P<slug>[\w\._-]+)/topics/create/$',
        view=   'iris.views.topic_create',
        kwargs= dict(
            VERIFIED_VOLUNTEER,
            post_topic_create=team_post_topic_create,
        ),
    ),
    url(regex=  r'^teams/',
        view=   include('teams.urls'),
        kwargs= dict(
            VERIFIED_VOLUNTEER,
            extra_context=dict(
                topic_create_form=TopicForm(),
            ),
        ),
    ),
)
urlpatterns += team_bridge.include_urls(
    'wakawaka.urls',
    r'^teams/(?P<team_slug>[\w\._-]+)/wiki/',
    kwargs=VERIFIED_VOLUNTEER,
)
urlpatterns += team_bridge.include_urls(
    'dregni.urls',
    r'^teams/(?P<team_slug>[\w\._-]+)/events/',
    kwargs=dict(
        VERIFIED_VOLUNTEER,
        event_delete_predicate=predicates.event_delete, # @@@ see swproject.predicates
        event_edit_predicate=predicates.event_edit,     # @@@ see swproject.predicates
        start_date=datetime.date.today,
        weeks=6,
        jump_weeks=4,
    ),
)


# Redirects
legacy_urls = (
    ('^wiki/', '/dashboard/'),

    ('^support/$', '/placeholder/support/'),
    ('^library/$', '/placeholder/library/'),
    ('^coordinators/$', '/placeholder/coordinators/'),
)
for oldurl, newurl in legacy_urls:
    urlpatterns += patterns('',
        url(oldurl, 'django.views.generic.simple.redirect_to', {'url': newurl}),
    )


# CMS at very end, to catch everything else.
urlpatterns += patterns('',
    url(r'^', include('cms.urls')),
)
