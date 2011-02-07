import datetime

from haystack import indexes
from haystack import site

from dregni.models import Event
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from iris.models import Item
from swtopics.models import Message
from teams.models import Team
from wakawaka.models import WikiPage

# Special Team IDs
# 0 -- not associated with a team, visible
# -1 -- not associated with a team, should be hidden


class AuthUserIndex(indexes.SearchIndex):

    text = indexes.CharField(document=True, use_template=True)
    team_id = indexes.IntegerField()

    def get_queryset(self):
        return User.objects.all()

    def prepare_team_id(self, obj):
        return 0

site.register(User, AuthUserIndex)


class CommentsCommentIndex(indexes.SearchIndex):

    text = indexes.CharField(document=True, model_attr='comment')
    team_id = indexes.IntegerField()
    created = indexes.DateTimeField(model_attr='submit_date')

    def get_queryset(self):
        return Comment.objects.all()

    def prepare_team_id(self, obj):
        try:
            content = obj.content_object
        except AttributeError:
            # Comments for content types that no longer exist.
            return -1
        # Comments about wiki pages.
        if isinstance(content, WikiPage):
            group = content.group
            return group.id if group else -1
        # Comments not tied to a group should be hidden.
        return -1

site.register(Comment, CommentsCommentIndex)


class DregniEventIndex(indexes.SearchIndex):

    text = indexes.CharField(document=True, use_template=True)
    team_id = indexes.IntegerField()
    created = indexes.DateTimeField(model_attr='created')
    modified = indexes.DateTimeField(model_attr='modified')

    def get_queryset(self):
        # Only include events that are attached to a group.
        return Event.objects.exclude(object_id=None)

    def prepare_team_id(self, obj):
        group = obj.group
        return group.id if group else -1

site.register(Event, DregniEventIndex)


class SwtopicsMessageIndex(indexes.SearchIndex):

    text = indexes.CharField(document=True, model_attr='text')
    team_id = indexes.IntegerField()
    created = indexes.DateTimeField()

    def get_queryset(self):
        return Message.objects.all()

    def prepare_created(self, obj):
        ct = ContentType.objects.get_for_model(obj)
        item = Item.objects.get(content_type=ct, object_id=obj.id)
        return item.created

    def prepare_team_id(self, obj):
        ct = ContentType.objects.get_for_model(obj)
        item = Item.objects.get(content_type=ct, object_id=obj.id)
        topic = item.topic
        team_participants = topic.participants_of_type(Team)
        team_id = None
        for p in team_participants:
            team = p.content
            if not team.is_private:
                return team.id
            team_id = team.id
        return team_id if team_id else -1

site.register(Message, SwtopicsMessageIndex)


class WakawakaWikiPageIndex(indexes.SearchIndex):

    text = indexes.CharField(document=True, use_template=True)
    team_id = indexes.IntegerField()
    slug = indexes.CharField(model_attr='slug')
    created = indexes.DateTimeField(model_attr='created')
    modified = indexes.DateTimeField(model_attr='modified')

    def get_queryset(self):
        # Only include wiki pages that are attached to a group.
        return WikiPage.objects.exclude(object_id=None)

    def prepare_team_id(self, obj):
        group = obj.group
        return group.id if group else -1

site.register(WikiPage, WakawakaWikiPageIndex)
