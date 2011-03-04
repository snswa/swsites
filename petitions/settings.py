from django.conf import settings


# Maximum number of signature collector IDs allowed.
MAX_COLLECTOR_IDS = getattr(settings, 'PETITIONS_MAX_COLLECTOR_IDS', 1)

CHECKSUM_DIGIT_MAP = getattr(settings, 'PETITIONS_CHECKSUM_DIGIT_MAP', 'AEGJNPSTWX')
