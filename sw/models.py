from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify

from idios.models import ProfileBase


class Profile(ProfileBase):

    PRIVACY_CHOICES_PCFA = [
        ('P', 'Private'),
        ('C', 'Coordinators only'),
        ('F', 'Friends and coordinators'),
        ('A', 'All volunteers'),
    ]

    PRIVACY_CHOICES_CFA = [
        ('C', 'Coordinators only'),
        ('F', 'Friends and coordinators'),
        ('A', 'All volunteers'),
    ]

    preferred_name = models.CharField(max_length=50, blank=True,
        help_text='How your name will appear to all volunters.')

    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    name_privacy = models.CharField(max_length=1, choices=PRIVACY_CHOICES_PCFA, default='C')

    zip_code = models.CharField(max_length=30, blank=True)
    zip_code_privacy = models.CharField(max_length=1, choices=PRIVACY_CHOICES_CFA, default='C')

    mailing_address = models.TextField(blank=True)
    mailing_address_privacy = models.CharField(max_length=1, choices=PRIVACY_CHOICES_PCFA, default='C')

    email_privacy = models.CharField(max_length=1, choices=PRIVACY_CHOICES_PCFA, default='C',
        help_text='Manage email addresses by saving your profile, then clicking "Manage Email Addresses".')

    phone_number = models.CharField(max_length=20, blank=True)
    phone_number_accepts_texts = models.BooleanField(default=False)
    phone_number_privacy = models.CharField(max_length=1, choices=PRIVACY_CHOICES_PCFA, default='C')

    yahoo_messenger = models.CharField(max_length=100, blank=True)
    aim = models.CharField(max_length=100, blank=True)
    msn_messenger = models.CharField(max_length=100, blank=True)
    skype = models.CharField(max_length=100, blank=True)
    messaging_privacy = models.CharField(max_length=1, choices=PRIVACY_CHOICES_CFA, default='C')

    preferred_contact_methods = models.CharField(max_length=255, blank=True)
    preferred_contact_methods_privacy = models.CharField(max_length=1, choices=PRIVACY_CHOICES_CFA, default='C')

    bio = models.TextField(blank=True)
    bio_privacy = models.CharField(max_length=1, choices=PRIVACY_CHOICES_CFA, default='C')

    occupation = models.CharField(max_length=100, blank=True)
    occupation_privacy = models.CharField(max_length=1, choices=PRIVACY_CHOICES_PCFA, default='C')
    employer = models.CharField(max_length=100, blank=True)
    employer_privacy = models.CharField(max_length=1, choices=PRIVACY_CHOICES_PCFA, default='C')

    def __unicode__(self):
        return self.preferred_name or self.user.username


# ========================================================================
# Overrides and extensions

from wakawaka.models import Revision

def __unicode__(self):
    return self.page.slug
Revision.__unicode__ = __unicode__
