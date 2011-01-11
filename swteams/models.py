from django.contrib.auth.models import User
from django.db import models

from teams.models import Member


# class TeamPageEditor(models.Model):
#     """A team member who can edit team pages."""
#
#     member = models.ForeignKey(Member)
#
#     class Meta:
#         pass
#
#     def __unicode__(self):
#         return u"TeamPageEditor"
#
#
# class TeamEventEditor(models.Model):
#     """A team member who can edit team events."""
#
#     member = models.ForeignKey(Member)
#
#     class Meta:
#         pass
#
#     def __unicode__(self):
#         return u"TeamEventsEditor"
#
#
# class TeamTopicModerator(models.Model):
#     """A team member who can remove a team from a topic's participant list."""
#
#     member = models.ForeignKey(Member)
#
#     class Meta:
#         pass
#
#     def __unicode__(self):
#         return u"TeamTopicsModerator"
