from django.conf import settings
from django.db.models.signals import post_save, pre_delete
from django.utils.text import truncate_words

from django.contrib.auth.models import Group, User
from django.contrib.comments.signals import comment_was_posted

from actstream import action

from attachments.models import Attachment

from teams.models import Member

from wakawaka.models import Revision, WikiPage


# ====================================================================
# Auto join users to groups specified in settings.AUTO_JOIN_GROUPS

def auto_join_user_to_groups(sender, instance, created, **kwargs):
    if created:
        for group_name in settings.AUTO_JOIN_GROUPS:
            try:
                group = Group.objects.get(name=group_name)
            except Group.DoesNotExist:
                pass
            else:
                instance.groups.add(group)

post_save.connect(auto_join_user_to_groups, sender=User)


# ====================================================================
# Activity stream

def stream_wiki_attachment(sender, instance, created, **kwargs):
    if created:
        obj = instance.content_object
        if isinstance(obj, WikiPage):
            action.send(
                instance.creator,
                verb='attached file {0} to wiki page'.format(instance.filename),
                action_object=obj,
                target=obj.group,
                timestamp=instance.created,
            )

post_save.connect(stream_wiki_attachment, sender=Attachment)


def stream_wiki_comment(sender, comment, request, **kwargs):
    obj = comment.content_object
    if isinstance(obj, WikiPage):
        action.send(
            comment.user,
            verb='commented on wiki page',
            action_object=obj,
            target=obj.group,
            timestamp=comment.submit_date,
            description=truncate_words(comment.comment, 25),
        )

comment_was_posted.connect(stream_wiki_comment)


def stream_wiki_revision(sender, instance, created, **kwargs):
    if created:
        action.send(
            instance.creator,
            verb='changed wiki page',
            action_object=instance,
            target=instance.page.group,
            timestamp=instance.modified,
            description=instance.message,
        )

post_save.connect(stream_wiki_revision, sender=Revision)


def stream_team_join(sender, instance, created, **kwargs):
    if created:
        action.send(
            instance.user,
            verb='joined team',
            target=instance.team,
        )

post_save.connect(stream_team_join, sender=Member)


def stream_team_leave(sender, instance, **kwargs):
    action.send(
        instance.user,
        verb='left team',
        target=instance.team,
    )

pre_delete.connect(stream_team_leave, sender=Member)
