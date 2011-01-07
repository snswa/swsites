from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from iris.models import Topic
from teams.models import Team


def team_post_topic_create(request, topic, *args, **kwargs):
    # Instead of adding the user as a participant, add the group
    # instead.
    team = get_object_or_404(Team, slug=kwargs['slug'])
    topic.add_participant(creator=request.user, obj=team)


def team_topics_queryset_fn(request, queryset, *args, **kwargs):
    content_type = ContentType.objects.get_for_model(Team)
    team = Team.objects.get(slug=kwargs['slug'])  # get team from URL
    return Topic.objects.filter(
        participants__content_type=content_type,
        participants__object_id=team.id,
    )
