from swproject.settings import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES['default']['NAME'] = 'swdev'
DATABASES['default']['USER'] = 'user'
DATABASES['default']['PASSWORD'] = 'password'
DATABASES['default']['HOST'] = '/var/run/postgresql'

SKIP_SOUTH_TESTS = True
SOUTH_TESTS_MIGRATE = False

CELERY_ALWAYS_EAGER = True

if django.VERSION >= (1, 3):
    STATICFILES_ROOT = 'static'
else:
    STATIC_ROOT = 'static'

from fnmatch import fnmatch
class glob_list(list):
    def __contains__(self, key):
        for elt in self:
            if fnmatch(key, elt): return True
        return False

INTERNAL_IPS = glob_list([
    '*.*.*.*',
])

SENTRY_TESTING = False

MEDIA_PATH = 'uploaded_media/'

CMS_PAGE_MEDIA_PATH = 'cms_page_media/'

ZINNIA_UPLOAD_TO = 'blog_uploads/'

STATICFILES_DIRS = (
    ('uploaded_media', 'uploaded_media'),
)

STATICFILES_RESOLVERS += (
    'staticfiles.resolvers.FileSystemResolver',
)

POSTMARK_DEBUG = True

HAYSTACK_SEARCH_ENGINE = 'solr'
HAYSTACK_SOLR_URL = 'http://127.0.0.1:8080/solr'

### Suggested additions to your localsettings.py ###

# ----
# concurrent server
#
# $ pip install -e git+git://github.com/ashchristopher/django-concurrent-server.git#egg=django-concurrent-server
#
# INSTALLED_APPS += (
#     'concurrent_server',
# )
#
# ----
# Devserver
#
# $ pip install git+git://github.com/dcramer/django-devserver#egg=django-devserver
# $ pip install sqlparse
# $ pip install werkzeug
# $ pip install guppy
#

# INSTALLED_APPS += (
#     'devserver',
# )
#
# DEVSERVER_MODULES = (
#     'devserver.modules.sql.SQLRealTimeModule',
#     'devserver.modules.sql.SQLSummaryModule',
#     'devserver.modules.profile.ProfileSummaryModule',
#     # Modules not enabled by default
#     ## 'devserver.modules.ajax.AjaxDumpModule',
#     ## 'devserver.modules.profile.MemoryUseModule',
#     ## 'devserver.modules.cache.CacheSummaryModule',
# )

# ----
# Debug toolbar
#
# $ pip install django-debug-toolbar
#

# MIDDLEWARE_CLASSES += (
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
# )
#
# INSTALLED_APPS += (
#     'debug_toolbar',
# )
#
# DEBUG_TOOLBAR_CONFIG = {
#     'INTERCEPT_REDIRECTS': False,
# }
