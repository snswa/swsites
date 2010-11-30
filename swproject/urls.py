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
## handler500 = ...


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
    # Deployment tests:
    url(r'^_site/', include('sw.urls')),
    #
    # Accounts:
    url(r'^accounts/', include('allauth.urls')),
    #
    # Admin:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    #
    # Sentry:
    url(r'^sentry/', include('sentry.urls')),
    #
    # Blog:
    url(r'^blog/', include('zinnia.urls')),
    #
    # Comments:
    url(r'^comments/', include('django.contrib.comments.urls')),
    #
    # Wakawaka (wiki):
    url(r'^wiki/', include('swproject.urls_wiki')),
    #
    # djangovoice (feedback):
    url(r'^feedback/', include('djangovoice.urls')),
    #
    # haystack (search):
    url(r'^search/', include('swproject.urls_search')),
    #
    # idios (profiles):
    url(r'^profiles/', include('idios.urls')),
    #
    # dashboard:
    url(r'^dashboard/', include('dashboard.urls')),
    #
    # teams:
    url(r'^teams/', include('teams.urls')),
)


# Bridged URLs.
urlpatterns += wiki_bridge.include_urls(
    'swproject.urls_team_wiki',
    r'^teams/(?P<team_slug>[\w\._-]+)/wiki/',
)


# Legacy redirects and CMS at very end, to catch everything else.
urlpatterns += patterns('',
    #
    # CMS: catch everything else.
    url(r'^', include('cms.urls')),
    #
    # TODO: Legacy redirects from sensiblewashington.org site
)
