from django.db import models


class Message(models.Model):
    """A plain text discussion message."""

    text = models.TextField()

    def __unicode__(self):
        return u'Message'


class SubjectChange(models.Model):

    old_subject = models.CharField(max_length=255)
    new_subject = models.CharField(max_length=255)

    def __unicode__(self):
        return u"Subject change"
