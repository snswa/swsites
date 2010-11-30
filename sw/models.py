from django.db import models

from idios.models import ProfileBase


class Profile(ProfileBase):

    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)

    zip_code = models.CharField(max_length=5, blank=True)
    mailing_address = models.TextField(blank=True)

    phone_number = models.CharField(max_length=20, blank=True)

    yahoo_messenger = models.CharField(max_length=100, blank=True)
    aim = models.CharField(max_length=100, blank=True)
    msn_messenger = models.CharField(max_length=100, blank=True)
    skype = models.CharField(max_length=100, blank=True)

    preferred_contact_methods = models.CharField(max_length=255, blank=True)

    bio = models.TextField(blank=True)


# ========================================================================
# Overrides and extensions

from wakawaka.models import Revision

def __unicode__(self):
    return self.page.slug
Revision.__unicode__ = __unicode__
