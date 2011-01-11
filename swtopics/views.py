from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404

from dregni.models import Event
from iris.models import Topic
from teams.models import Team


# ---


def team_post_topic_create(request, topic, *args, **kwargs):
    # Instead of adding the user as a participant, add the group
    # instead.
    team = get_object_or_404(Team, slug=kwargs['slug'])
    topic.add_participant(creator=request.user, obj=team)


def team_topics_queryset_fn(request, queryset, *args, **kwargs):
    content_type = ContentType.objects.get_for_model(Team)
    team = get_object_or_404(Team, slug=kwargs['slug'])
    return Topic.objects.filter(
        participants__content_type=content_type,
        participants__object_id=team.id,
    )


# ---


def team_event_post_topic_create(request, topic, *args, **kwargs):
    # Instead of adding the user as a participant, add the event
    # instead.
    content_type = ContentType.objects.get_for_model(Team)
    team = get_object_or_404(Team, slug=kwargs['slug'])  # get team from URL
    event = get_object_or_404(Event,
        site=Site.objects.get_current(),
        content_type=content_type,
        object_id=team.id,
        id=kwargs['event_id'],
    )
    topic.add_participant(creator=request.user, obj=team)
    topic.add_participant(creator=request.user, obj=event)


def team_event_topics_queryset_fn(request, queryset, *args, **kwargs):
    event_content_type = ContentType.objects.get_for_model(Event)
    team_content_type = ContentType.objects.get_for_model(Team)
    team = get_object_or_404(Team, slug=kwargs['slug'])  # get team from URL
    event = get_object_or_404(Event,
        site=Site.objects.get_current(),
        content_type=team_content_type,
        object_id=team.id,
        id=kwargs['event_id'],
    )
    return Topic.objects.filter(
        participants__content_type=event_content_type,
        participants__object_id=event.id,
    )
