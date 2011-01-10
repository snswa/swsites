from django.db import models


class Message(models.Model):
    """A plain text discussion message."""

    text = models.TextField()

    def __unicode__(self):
        return u'Message'
