from django.conf import settings
from django.contrib.auth.models import Group, User
from django.contrib.comments.signals import comment_was_posted
from django.db.models.signals import post_save, pre_delete
from django.utils.text import truncate_words

from actstream import action
from attachments.models import Attachment
from dregni.models import Event
from iris.models import Item
from swtopics.models import Message
from teams.models import Member, Team
from wakawaka.models import Revision, WikiPage


TRUNCATE_WORDS = 15


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


def stream_event(sender, instance, created, **kwargs):
    if created:
        action.send(
            instance.creator,
            verb='created the event',
            action_object=instance,
            target=instance.group,
            timestamp=instance.modified,
            description=truncate_words(instance.description, TRUNCATE_WORDS) if instance.description else None,
        )
    else:
        action.send(
            instance.modifier,
            verb='changed the event',
            action_object=instance,
            target=instance.group,
            timestamp=instance.modified,
        )

post_save.connect(stream_event, sender=Event)


def stream_event_comment(sender, comment, request, **kwargs):
    obj = comment.content_object
    if isinstance(obj, Event):
        action.send(
            comment.user,
            verb='commented on the event',
            action_object=comment,
            target=obj.group,
            timestamp=comment.submit_date,
            description=truncate_words(comment.comment, TRUNCATE_WORDS),
        )

comment_was_posted.connect(stream_event_comment)


def stream_topic_item_message(sender, instance, created, **kwargs):
    if created:
        obj = instance.content
        if isinstance(obj, Message):
            topic = instance.topic
            print 'topic', topic
            print topic.participants_of_type(Team)
            for team_joined in topic.participants_of_type(Team):
                action.send(
                    instance.creator,
                    verb='added a message to',
                    action_object=topic,
                    target=team_joined.content,
                    timestamp=instance.created,
                    description=truncate_words(obj.text, TRUNCATE_WORDS)
                )

post_save.connect(stream_topic_item_message, sender=Item)


def stream_wiki_attachment(sender, instance, created, **kwargs):
    if created:
        obj = instance.content_object
        if isinstance(obj, WikiPage):
            action.send(
                instance.creator,
                verb='attached the file {0} to'.format(instance.filename),
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
            verb='commented on the page',
            action_object=comment,
            target=obj.group,
            timestamp=comment.submit_date,
            description=truncate_words(comment.comment, TRUNCATE_WORDS),
        )

comment_was_posted.connect(stream_wiki_comment)


def stream_wiki_revision(sender, instance, created, **kwargs):
    if created:
        action.send(
            instance.creator,
            verb='changed the page',
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
            verb='joined',
            target=instance.team,
        )

post_save.connect(stream_team_join, sender=Member)


def stream_team_leave(sender, instance, **kwargs):
    action.send(
        instance.user,
        verb='left',
        target=instance.team,
    )

pre_delete.connect(stream_team_leave, sender=Member)
