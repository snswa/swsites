import django
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import redirect_to

if django.VERSION >= (1, 3):
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
else:
    from staticfiles.urls import staticfiles_urlpatterns


admin.autodiscover()


handler404 = 'swlegacy.views.legacy_or_404'


urlpatterns = patterns('')


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()


urlpatterns += patterns('',
    # Example:
    # (r'^swproject/', include('swproject.foo.urls')),
    #
    # Deployment tests:
    (r'^_site/', include('swsite.urls')),
    #
    # Accounts:
    (r'^accounts/', include('allauth.urls'), {'SSL': True}),
    #
    # Admin:
    (r'^admin/doc/', include('django.contrib.admindocs.urls'), {'SSL': True}),
    (r'^admin/', include(admin.site.urls), {'SSL': True}),
    #
    # Sentry:
    (r'^sentry/', include('sentry.urls'), {'SSL': True}),
    #
    # New index prototype.
    (r'^newindex', 'swsite.views.newindex', {}, 'index'),
    #
    # Blog:
    (r'^blog/', include('zinnia.urls')),
    #
    # Comments:
    (r'^comments/', include('django.contrib.comments.urls')),
    #
    # # Wiki:
    # (r'^wiki/', include('wiki.urls'), {'SSL': True}),
    #
    # # Notifications:
    # (r'^notification/', include('notification.urls')),
    #
    # Wakawaka (wiki):
    (r'^wiki/', include('swproject.urls_wiki'), {'SSL': True}),
    #
    # djangovoice (feedback):
    (r'^feedback/', include('djangovoice.urls'), {'SSL': True}),
    #
    # haystack (search):
    (r'^search/', include('swproject.urls_search')),
    #
    # TODO: Legacy redirects from sensiblewashington.org site
    #
    # CMS: catch everything else.
    (r'^', include('cms.urls')),
)
