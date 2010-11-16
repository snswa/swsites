from django.conf import settings


VALID_DOMAINS = getattr(settings, 'EMAILFWD_VALID_DOMAINS', [])
DEFAULT_DOMAIN = getattr(settings, 'EMAILFWD_DEFAULT_DOMAIN', None)
