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
from sw.forms import ProfileForm
from swproject import predicates
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
wiki_bridge = ContentBridge(Team, 'wakawaka')


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
    url(r'^_site/', include('sw.urls')),    # Deployment tests and temporary views.

    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^sentry/', include('sentry.urls')),

    # Figure out how to mesh these two together for login.
    url(r'^accounts/', include('allauth.urls'), kwargs=dict(
        email_preferred=True,
        profile_preferred=True,
    )),
    url(r'^hq/', 'sw.views.hq', name='sw_hq'),

    url(r'^attachments/', include('attachments.urls'), kwargs=VERIFIED_VOLUNTEER),
    url(r'^comments/', include('django.contrib.comments.urls'), kwargs=VERIFIED_VOLUNTEER),
    url(r'^dashboard/', include('dashboard.urls'), kwargs=VERIFIED_VOLUNTEER),
    url(r'^features/', include('featurelabs.urls'), kwargs=VERIFIED_VOLUNTEER),
    url(r'^local/', include('swlocal.urls'), kwargs=NEW_VOLUNTEER),
    url(r'^placeholder/', include('swproject.urls_placeholders'), kwargs=VERIFIED_VOLUNTEER),
    url(r'^profiles/', include('idios.urls'), kwargs=dict(
        NEW_VOLUNTEER,
        form_class=ProfileForm,
    )),
    url(r'^relationships/', include('relationships.urls'), kwargs=NEW_VOLUNTEER),
    url(r'^search/', include('swproject.urls_search'), kwargs=VERIFIED_VOLUNTEER),
    url(r'^teams/', include('teams.urls'), kwargs=VERIFIED_VOLUNTEER),
    url(r'^teams/(?P<slug>[\w\._-]+)/activity/$', view='sw.views.team_activity_history', name='team_activity_history', kwargs=VERIFIED_VOLUNTEER),
    url(r'^voting/', include('voting.urls'), kwargs=VERIFIED_VOLUNTEER),
)


# Bridged URLs.
urlpatterns += wiki_bridge.include_urls('wakawaka.urls',
    r'^teams/(?P<team_slug>[\w\._-]+)/wiki/',
    kwargs=VERIFIED_VOLUNTEER,
)
urlpatterns += wiki_bridge.include_urls('dregni.urls',
    r'^teams/(?P<team_slug>[\w\._-]+)/events/',
    kwargs=dict(
        VERIFIED_VOLUNTEER,
        event_delete_predicate=predicates.event_delete,
        event_edit_predicate=predicates.event_edit,
        start_date=datetime.date.today,
        weeks=6,
        jump_weeks=4,
    ),
)


# Redirects
legacy_urls = (
    ('^wiki/', '/dashboard/'),

    ('^local/$', '/placeholder/local/'),
    ('^state/$', '/placeholder/state/'),
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
