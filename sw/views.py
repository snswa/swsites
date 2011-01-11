from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext
from django.template import TemplateDoesNotExist, TemplateSyntaxError
from django.views.generic.list_detail import object_list

from actstream import action
from actstream.templatetags.activity_tags import actionsisactorof
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


# -- activity stream --


@login_required
def user_team_activity(request, username, template_name='idios/profile_activity.html', extra_context=None, *args, **kw):
    extra_context = extra_context or {}
    page_user = User.objects.get(username=username)
    team_ct = ContentType.objects.get_for_model(Team)
    queryset = actionsisactorof(page_user).filter(target_content_type=team_ct)
    extra_context['page_user'] = page_user
    return object_list(
        request,
        queryset=queryset,
        template_name=template_name,
        extra_context=extra_context,
        *args, **kw
    )
