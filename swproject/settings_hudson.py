from swproject.settings import *


DATABASES['default']['NAME'] = 'hudson'
DATABASES['default']['USER'] = 'hudson'
DATABASES['default']['HOST'] = 'localhost'

CELERY_ALWAYS_EAGER = True
