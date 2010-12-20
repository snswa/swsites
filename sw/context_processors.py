from actstream.models import Action

from teams.models import Team

from wakacmsplugin.settings import TEAM_SLUG

from wakawaka.models import WikiPage
from wakawaka.settings import DEFAULT_INDEX


def missing_info(request):
    return {'missing_info': request.missing_info}


def team_actions(request):
    """Add a `team_actions` queryset for the current context's team."""
    if isinstance(request.group, Team):
        return {
            'team_actions': request.group.content_objects(Action, gfk_field='target').order_by('-timestamp'),
        }
    else:
        return {}


def team_membership(request):
    """Add `is_team_member` if the user is a member of the context's team."""
    if isinstance(request.group, Team):
        return {
            'is_team_member': request.group.user_is_member(request.user),
            'team_membership': request.group.member_set.filter(user=request.user),
        }
    else:
        return {}


def team_wakacms_membership(request):
    """Add `is_wakacms_team_member` if the user is a member of the team named
    in WAKACMSPLUGIN_TEAM_SLUG."""
    team = Team.objects.get(slug=TEAM_SLUG)
    return {
        'is_wakacms_team_member': team.user_is_member(request.user),
    }


def team_wiki_index_page(request):
    """Add `team_wiki_index_page` for the context's team,
    containing the default wiki page for the team."""
    if isinstance(request.group, Team):
        # Find wiki index.
        try:
            page = request.group.content_objects(WikiPage).get(slug=DEFAULT_INDEX)
        except WikiPage.DoesNotExist:
            page = None
        return {
            'team_wiki_index_page': page,
        }
    else:
        return {}
