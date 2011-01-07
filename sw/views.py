from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext
from django.template import TemplateDoesNotExist, TemplateSyntaxError

from actstream import action
from allauth.account.forms import LoginForm
from sw.forms import HqSignupForm
from sw.tasks import report_ok
from teams.models import Team
from wakawaka.models import WikiPage


def report_ok_view(request):
    content = report_ok.delay().get()
    return HttpResponse(content, mimetype='text/plain')


# --- HQ ---


def hq(request, *args, **kw):
    template_name = 'sw/hq.html'
    #
    # Direct to dashboard if logged in already
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('dashboard_index'))
    # Prepare signup form.
    if request.method == 'POST':
        signup_form = HqSignupForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save(request=request)
            # Sign in right away.
            data = signup_form.cleaned_data
            user = authenticate(
                username=data['username'],
                password=data['password1'],
            )
            login(request, user)
            return HttpResponseRedirect(reverse('profile_edit'))
    else:
        signup_form = HqSignupForm()
    # Prepare login form.
    login_form = LoginForm()
    # Finish.
    template_context = {
        'login_form': login_form,
        'signup_form': signup_form,
    }
    return render_to_response(
        template_name,
        template_context,
        RequestContext(request),
    )


# -- placeholders --


def placeholder(request, slug, *args, **kw):
    template_name = 'sw/placeholders/{0}.html'.format(slug)
    template_context = {
    }
    try:
        return render_to_response(
            template_name,
            template_context,
            RequestContext(request),
        )
    except TemplateDoesNotExist:
        raise Http404()


# -- activity history --


def team_activity_history(request, slug, *args, **kw):
    template_name = 'teams/activity.html'
    team = get_object_or_404(Team, slug=slug)
    template_context = {
        'group': team,
    }
    return render_to_response(template_name, template_context, RequestContext(request))


# -- topics --


def team_post_topic_create(request, topic, *args, **kwargs):
    # Instead of adding the user as a participant, add the group
    # instead.
    team = get_object_or_404(Team, slug=kwargs['slug'])
    topic.add_participant(creator=request.user, obj=team)
