from actstream.models import Action

from teams.models import Team


def team_actions(request):
    if isinstance(request.group, Team):
        return {
            'team_actions': request.group.content_objects(Action, gfk_field='target').order_by('-timestamp'),
        }
    else:
        return {}


def team_membership(request):
    if isinstance(request.group, Team):
        return {
            'is_team_member': request.group.user_is_member(request.user),
        }
    else:
        return {}
