import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from dashboard.forms import DigestRangeForm
from dashboard.models import team_actions_for_user, team_topics_for_user, team_events_for_user
from dregni.models import Event
import dregni.views
from iris.models import Topic


TIME_FORMAT = '%Y-%m-%d %H:%M'


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


@login_required
def digest(request, form_class=DigestRangeForm, template_name='dashboard/digest.html', *args, **kwargs):
    now = datetime.datetime.now()
    start_date = None
    end_date = None
    mimetype = None
    if 'submit' in request.GET:
        form = form_class(request.GET)
        if form.is_valid():
            start_date = datetime.datetime.strptime(form.cleaned_data['start_date'], TIME_FORMAT)
            end_date = datetime.datetime.strptime(form.cleaned_data['end_date'], TIME_FORMAT)
            # Enforce max 7 days.
            if end_date - start_date > datetime.timedelta(days=7):
                start_date = end_date - datetime.timedelta(days=7)
    else:
        form = form_class(initial=dict(
            start_date=now - datetime.timedelta(days=1),
            end_date=now,
        ))
    template_context = dict(
        form=form,
    )
    if start_date and end_date:
        user = request.user
        # For each team the user is a member of, starting with their coordinator
        # teams and then the rest of the teams...
        teams = [member.team for member in user.member_set.filter(is_coordinator=True)]
        teams.extend(member.team for member in user.member_set.filter(is_coordinator=False))
        team_info_list = []
        for team in teams:
            new_members = User.objects.filter(
                member__team=team,
                member__joined__gte=start_date,
                member__joined__lte=end_date,
            )
            events = team.content_objects(Event).filter(
                start_date__gte=start_date.date() - datetime.timedelta(days=4),
                start_date__lte=end_date.date() + datetime.timedelta(days=14),
            )
            topics = Topic.objects.with_participant(team).filter(
                modified__gte=start_date,
                modified__lte=end_date,
            )
            team_info_list.append(dict(
                team=team,
                new_members=new_members,
                events=events,
                topics=topics,
            ))
        template_context.update(
            start_date=start_date,
            end_date=end_date,
            team_info_list=team_info_list,
        )
    if request.GET.get('submit') == 'email':
        pass
    else:
        if request.GET.get('submit') == 'html':
            template_name = 'dashboard/digest_html.html'
        if request.GET.get('submit') == 'plaintext':
            template_name = 'dashboard/digest_plaintext.txt'
            mimetype = 'text/plain'
        return render_to_response(template_name, template_context, RequestContext(request), mimetype=mimetype)
