from swproject.settings import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES['default']['NAME'] = 'swdev'
DATABASES['default']['USER'] = 'user'
DATABASES['default']['PASSWORD'] = 'password'
DATABASES['default']['HOST'] = '/var/run/postgresql'

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

SENTRY_TESTING = True

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INSTALLED_APPS += (
    'debug_toolbar',
)

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

HAYSTACK_SEARCH_ENGINE = 'whoosh'
import os
import swproject
HAYSTACK_WHOOSH_PATH = os.path.join(
    os.path.dirname(swproject.__file__),
    os.pardir,
    'whoosh_index',
)
