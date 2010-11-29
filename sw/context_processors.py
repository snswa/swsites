from teams.models import Team


def team_membership(request):
    if isinstance(request.group, Team):
        return {
            'is_team_member': request.group.user_is_member(request.user),
        }
    else:
        return {}