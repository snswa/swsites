from swproject.settings import *

DEBUG = False
TEMPLATE_DEBUG = True

# We require sign-in to be over SSL, but we want people to stay signed in
# even on non-SSL pages.
SESSION_COOKIE_SECURE = False
