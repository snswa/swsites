from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import Q

from actstream.models import Action
from dregni.models import Event
from iris.models import Topic
from teams.models import Team


def team_actions_for_user(user):
    q = None
    team_ct = ContentType.objects.get_for_model(Team)
    for team in user.team_set.all():
        subq = Q(target_content_type=team_ct) & Q(target_object_id=team.id)
        q = subq if q is None else q | subq
    if q is not None:
        team_actions = Action.objects.filter(q).order_by('-timestamp')
    else:
        team_actions = []
    return team_actions


def team_topics_for_user(user):
    q = None
    team_ct = ContentType.objects.get_for_model(Team)
    for team in user.team_set.all():
        subq = (
            Q(participants__content_type=team_ct)
            & Q(participants__object_id=team.id)
            & Q(participants__is_active=True)
        )
        q = subq if q is None else q | subq
    if q is not None:
        team_topics = Topic.objects.filter(q).order_by('-modified').distinct()
    else:
        team_topics = []
    return team_topics


def team_events_for_user(user):
    q = None
    site = Site.objects.get_current()
    team_ct = ContentType.objects.get_for_model(Team)
    for team in user.team_set.all():
        subq = Q(content_type=team_ct) & Q(object_id=team.id)
        q = subq if q is None else q | subq
    if q is not None:
        q &= Q(site=site)
        team_events = Event.objects.filter(q).order_by('-modified')
    else:
        team_events = []
    return team_events
