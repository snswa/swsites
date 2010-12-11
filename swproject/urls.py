# Top-level URLs

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

from teams.models import Team


admin.autodiscover()


# Site-wide error handlers.
handler404 = 'swlegacy.views.legacy_or_404'
handler500 = 'django.views.defaults.server_error'


# Begin with empty patterns.
urlpatterns = patterns('')

# Serve static files in debug mode.
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

# Group bridges
wiki_bridge = ContentBridge(Team, 'wakawaka')


urlpatterns += patterns('',
    # Example:
    # (r'^swproject/', include('swproject.foo.urls')),
    #
    url(r'^_site/', include('sw.urls')),    # Deployment tests and temporary views.
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^attachments/', include('attachments.urls')),
    # @@@ disabled, kept here to remind ourselves to remove zinnia
    # url(r'^blog/', include('zinnia.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^features/', include('featurelabs.urls')),
    url(r'^feedback/', include('djangovoice.urls')),
    url(r'^profiles/', include('idios.urls')),
    url(r'^search/', include('swproject.urls_search')),
    url(r'^sentry/', include('sentry.urls')),
    url(r'^teams/', include('teams.urls')),
    url(r'^voting/', include('voting.urls')),
)


# Bridged URLs.
urlpatterns += wiki_bridge.include_urls(
    'swproject.urls_team_wiki',
    r'^teams/(?P<team_slug>[\w\._-]+)/wiki/',
)


# Redirects
legacy_urls = (
    ('^wiki/', '/dashboard/'),
)
for oldurl, newurl in legacy_urls:
    urlpatterns += patterns('',
        url(oldurl, 'django.views.generic.simple.redirect_to', {'url': newurl}),
    )


# CMS at very end, to catch everything else.
urlpatterns += patterns('',
    url(r'^', include('cms.urls')),
)
