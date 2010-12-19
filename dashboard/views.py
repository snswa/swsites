from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from actstream.models import Action

from teams.models import Team


@login_required
def index(request):
    template_name = 'dashboard/index.html'
    # Chain together queries to find all team activities.
    q = None
    team_ct = ContentType.objects.get(app_label='teams', model='team')
    for team in request.user.team_set.all():
        subq = Q(target_content_type=team_ct) & Q(target_object_id=team.id)
        if q is None:
            q = subq
        else:
            q |= subq
    if q is not None:
        team_actions = Action.objects.filter(q).order_by('-timestamp')
    else:
        team_actions = []
    template_context = {
        'team_actions': team_actions,
    }
    return render_to_response(
        template_name,
        template_context,
        RequestContext(request),
    )
