from actstream.models import Action

from teams.models import Team

from wakawaka.models import WikiPage
from wakawaka.settings import DEFAULT_INDEX


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


def team_wiki_index_page(request):
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
