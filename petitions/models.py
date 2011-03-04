from django.contrib.auth.models import User
from django.db import models

from baluhn import generate

from petitions.settings import CHECKSUM_DIGIT_MAP


class Petition(models.Model):
    """An individual petition."""

    digits = models.IntegerField()
    printed = models.BooleanField(default=False)
    custodian = models.ForeignKey(User)

    class Meta:
        pass

    def __unicode__(self):
        return u"Petition"



class Transmittal(models.Model):
    """A movement of a petition from one user to another."""

    user_from = models.ForeignKey(User, related_name='transmittals_from')
    user_to = models.ForeignKey(User, related_name='transmittals_to')
    petition = models.ForeignKey(Petition)

    class Meta:
        pass

    def __unicode__(self):
        return u"Transmittal"
