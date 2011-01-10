from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from dashboard.models import team_actions_for_user, team_topics_for_user, team_events_for_user
import dregni.views


@login_required
def index(request, template_name='dashboard/index.html'):
    user = request.user
    team_actions = team_actions_for_user(user)
    team_topics = team_topics_for_user(user)
    team_events = team_events_for_user(user)
    template_context = {
        'team_actions': team_actions,
        'team_topics': team_topics,
        'team_events': team_events,
    }
    return render_to_response(
        template_name,
        template_context,
        RequestContext(request),
    )


@login_required
def actions(request, template_name='dashboard/actions.html'):
    user = request.user
    team_actions = team_actions_for_user(user)
    template_context = {
        'object_list': team_actions,
    }
    return render_to_response(template_name, template_context, RequestContext(request))


@login_required
def topics(request, template_name='dashboard/topics.html'):
    user = request.user
    team_topics = team_topics_for_user(user)
    template_context = {
        'object_list': team_topics,
    }
    return render_to_response(template_name, template_context, RequestContext(request))


@login_required
def events(request, template_name='dashboard/events.html', *args, **kwargs):
    user = request.user
    team_events = team_events_for_user(user)
    return dregni.views.index(
        request,
        template_name=template_name,
        filter_qs=lambda qs: team_events,
        *args, **kwargs
    )
