import os
from datetime import timedelta

import django
from django.utils.translation import ugettext_lazy as _

from celery.schedules import crontab

# Bump this to force reloading of static media tagged with
# ?{{ MEDIA_SERIAL_NUMBER }} on next deploy.
MEDIA_SERIAL_NUMBER = '2011011301'

DEBUG = False
TEMPLATE_DEBUG = True

ADMINS = ()

CONTACT_EMAIL = 'webmaster@sensiblewashington.org'

SENTRY_ADMINS = (
    ('Matthew Scott', 'matt@11craft.com'),
)

MANAGERS = SENTRY_ADMINS

SENTRY_CATCH_404_ERRORS = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '5432',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'replace this value in a production environment'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.media.PlaceholderMediaMiddleware',
    'groups.middleware.GroupAwareMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'featureflipper.middleware.FeaturesMiddleware',
    'sw.middleware.HqPredicateMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',

    'allauth.account.context_processors.account',

    'cms.context_processors.media',

    'sw.context_processors.media_serial_number',
    'sw.context_processors.team_wakacms_membership',
    'sw.context_processors.team_wiki_index_page',

    'featureflipper.context_processors.features',
)

AUTHENTICATION_BACKENDS = (
    'swproject.predicates.TopicAccessBackend',
    'swproject.predicates.WikiAccessBackend',
    'teams.backends.TeamMembershipBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# ==================================================================
# Static files

if django.VERSION < (1, 3):
    TEMPLATE_CONTEXT_PROCESSORS += (
        'staticfiles.context_processors.static_url',
    )
    STATICFILES_RESOLVERS = (
        'staticfiles.resolvers.AppDirectoriesResolver',
    )

ROOT_URLCONF = 'swproject.urls'

TEMPLATE_DIRS = (
    # We put all of our templates in apps, including the swtemplates app
    # for top-level templates.
)

if django.VERSION >= (1, 3):
    STATICFILES_URL = MEDIA_URL
else:
    STATIC_URL = MEDIA_URL

# =================================================================
# Tests

TEST_RUNNER = 'swproject.testing.CustomTestSuiteRunner'

# =================================================================
# Cache

CACHE_BACKEND = 'locmem:///?max_entries=5000'

# ==================================================================
# url overrides

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda o: '/profiles/profile/%s/' % o.username,
}

# =================================================================
# auth

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = True

LOGIN_REDIRECT_URL = '/dashboard/'

AUTO_JOIN_GROUPS = [
    'allusers',
    # 'wiki.editor',
]

# =================================================================
# django-cms

CMS_TEMPLATES = (
    ('cms/c12.html', _('content 12')),
    ('cms/s4_c8.html', _('sidebar 4, content 8')),
    ('cms/c4_c4_c4.html', _('content 4, content 4, content 4')),
    ('cms/c6_c6.html', _('content 6, content 6')),
    ('cms/c8_s4.html', _('content 8, sidebar 4')),
    ('cms/l12_s4_c8.html', _('lead-in 12 / sidebar 4, content 8')),
    ('cms/l12_c6_c6.html', _('lead-in 12 / content 6, content 6')),
    ('cms/l12_c8_s4.html', _('lead-in 12 / content 8, sidebar 4')),
)

LANGUAGES = (
    ('en', _('US English')),
)

LANGUAGE_CODE = 'en'

APPEND_SLASH = True

# ==================================================================
# comments

COMMENTS_APP = 'sw.custom_comments'

# ==================================================================
# wakawaka (wiki)

WAKAWAKA_REQUIRE_TEAM_ROLE = ('wiki', 'member')

WAKAWAKA_EDITOR_COLUMNS = 70

# This applies to URL matching only, not to parsing pages.
WAKAWAKA_SLUG_REGEX = r'([ \w\._-]+)'

WAKAWAKA_DEFAULT_INDEX = 'TeamHomePage'

# ==================================================================
# waka cms plugin

# The slug of the team to grab wiki content snippets from, or None
# to use the global wiki.
WAKACMSPLUGIN_TEAM_SLUG = 'webcontent'

# ==================================================================
# postmark, email

DEFAULT_FROM_EMAIL = 'Sensible Washington <webmaster@sensiblewashington.org>'
SERVER_EMAIL = 'Sensible Washington <webmaster@sensiblewashington.org>'

POSTMARK_API_KEY = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
POSTMARK_SENDER = DEFAULT_FROM_EMAIL
EMAIL_BACKEND = 'postmark.django_backend.EmailBackend'

EMAIL_CONFIRMATION_DAYS = 7

# ==================================================================
# emailfwd

EMAILFWD_VALID_DOMAINS = [
    ('sensiblewashington.org', '@sensiblewashington.org'),
]

EMAILFWD_DEFAULT_DOMAIN = 'sensiblewashington.org'

# ==================================================================
# Haystack (search)

HAYSTACK_SITECONF = 'swproject.search_sites'
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10
HAYSTACK_LIMIT_TO_REGISTERED_MODELS = False

# ==================================================================
# idios (profiles)

AUTH_PROFILE_MODULE = 'sw.Profile'

# ==================================================================
# featureflipper

FEATURES_FILE = os.path.join(os.path.dirname(__file__), 'features.json')

# ==================================================================
# planet

USER_AGENT = 'django-planet/0.1'

# ==================================================================
# celery

CELERYBEAT_SCHEDULE = {
    'Update all feeds every 2 hours': {
        'task': 'sw.tasks.update_all_planet_feeds',
        'schedule': timedelta(seconds=2 * 60 * 60),
    },
    'Update SW blog every 15 minutes': {
        'task': 'sw.tasks.update_planet_feed',
        'args': ('https://sensiblewashington.org/blog/feed/',),
        'schedule': timedelta(seconds=15 * 60),
    },
    'Send activity updates to users with 00/24 schedule': {
        'task': 'dashboard.tasks.send_emails_to_schedule',
        'args': ('00/24',),
        'schedule': crontab(minute=0, hour=0),
    },
    'Send activity updates to users with 06/24 schedule': {
        'task': 'dashboard.tasks.send_emails_to_schedule',
        'args': ('06/24',),
        'schedule': crontab(minute=0, hour=6),
    },
    'Send activity updates to users with 12/24 schedule': {
        'task': 'dashboard.tasks.send_emails_to_schedule',
        'args': ('12/24',),
        'schedule': crontab(minute=0, hour=12),
    },
    'Send activity updates to users with 18/24 schedule': {
        'task': 'dashboard.tasks.send_emails_to_schedule',
        'args': ('18/24',),
        'schedule': crontab(minute=0, hour=18),
    },
    'Send activity updates to users with 00/48 schedule': {
        'task': 'dashboard.tasks.send_emails_to_schedule',
        'args': ('00/48',),
        'schedule': crontab(minute=0, hour=0),
    },
}

# ==================================================================
# dregni (calendar)

FIRST_WEEKDAY = 'Sunday'

# ==================================================================
# iris (topics)

IRIS_ITEM_TYPE_PLUGINS = (
    'swtopics.plugins.MessageAddPlugin',
    'swtopics.plugins.ParticipantAddTeamPlugin',
    'swtopics.plugins.SubjectChangePlugin',
)

# ==================================================================
# url shortening

SHORTEN_MODELS = {
    'U': 'auth.user',
    'E': 'dregni.event',
    'T': 'iris.topic',
}

SHORT_BASE_URL = 'http://swhq.org/r/'

SHORTEN_FULL_BASE_URL = 'https://sensiblewashington.org/'

# ==================================================================

INSTALLED_APPS = (
    #
    # ORDER MATTERS.
    #
    # Project.
    'sw',
    'swlocal',
    #
    # Included in Django
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles' if django.VERSION >= (1, 3) else 'staticfiles',
    #
    # Infrastructure
    'djcelery',
    'gunicorn',
    'south',
    #
    # Used by multiple apps
    'pagination',
    'tagging',
    'taggit',
    #
    # Sentry
    'indexer',
    'paging',
    'sentry',
    'sentry.client',
    #
    # Authentication
    'emailconfirmation',
    'uni_form',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.twitter',
    'allauth.openid',
    'allauth.facebook',
    #
    # django-cms master
    'cms',
    'cms.plugins.text',
    'cms.plugins.picture',
    'cms.plugins.link',
    'cms.plugins.file',
    'cms.plugins.snippet',
    'cms.plugins.googlemap',
    'mptt',
    'publisher',
    'menus',
    'reversion',
    #
    # wakawaka (wiki)
    'wakawaka',
    'django_markup',
    'wakacmsplugin',
    #
    'voting',
    'gravatar',
    #
    # Comment extensions
    'sw.custom_comments',
    #
    # Haystack (search)
    'haystack',
    #
    # email forwarding
    'emailfwd',
    #
    # idios (profiles)
    'idios',
    #
    # teams
    'teams',
    'groups',
    'swteams',
    #
    # activity stream
    'actstream',
    #
    # dashboard
    'dashboard',
    #
    # file attachments
    'attachments',
    #
    # feature flipping
    'featureflipper',
    'featurelabs',
    #
    'zipcodes',
    #
    # rss feed aggregation / display
    'atompub',
    'planet',
    'planetcms',
    #
    'relationships',
    #
    'dregni',
    #
    'iris',
    'swtopics',
    #
    'shorturls',
)
