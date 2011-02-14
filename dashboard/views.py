import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from dashboard import digests
from dashboard.forms import DigestRangeForm
from dashboard.models import all_events_for_user, team_actions_for_user, team_topics_for_user, team_events_for_user
from dashboard.tasks import send_email
from dregni.models import Event
import dregni.views
from iris.models import Topic


TIME_FORMAT = '%Y-%m-%d %H:%M'


@login_required
def index(request, template_name='dashboard/index.html'):
    user = request.user
    team_actions = team_actions_for_user(user)
    team_topics = team_topics_for_user(user)
    events = all_events_for_user(user)
    template_context = {
        'team_actions': team_actions,
        'team_topics': team_topics,
        'events': events,
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
    if 'teams' in request.GET:
        events = team_events_for_user(user)
    else:
        events = all_events_for_user(user)
    return dregni.views.index(
        request,
        template_name=template_name,
        filter_qs=lambda qs: events,
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
        template_context = digests.daily_context(user, start_date, end_date)
        if request.GET.get('submit') == 'html':
            template_name = 'dashboard/digest_html.html'
            return render_to_response(template_name, template_context, RequestContext(request))
        if request.GET.get('submit') == 'plaintext':
            template_name = 'dashboard/digest_plaintext.txt'
            return render_to_response(template_name, template_context, RequestContext(request), mimetype='text/plain')
        if request.GET.get('submit') == 'email':
            send_email.delay(user.id, start_date, end_date)
            return HttpResponse('Email will be sent if any activity detected.', mimetype='text/plain')
    else:
        return render_to_response(template_name, template_context, RequestContext(request))
