from django.conf import settings


TEAM_SLUG = getattr(settings, 'WAKACMSPLUGIN_TEAM_SLUG', None)
