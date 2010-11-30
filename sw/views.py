from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext

from actstream import action

from sw.tasks import report_ok

from teams.models import Team

from wakawaka.models import WikiPage


def report_ok_view(request):
    content = report_ok.delay().get()
    return HttpResponse(content, mimetype='text/plain')


@user_passes_test(lambda u: u.is_staff)
def temp_move_wiki_page(request):
    page_slug = request.POST.get('page_slug')
    team_slug = request.POST.get('team_slug')
    page = get_object_or_404(WikiPage, slug=page_slug, content_type=None, object_id=None)
    team = get_object_or_404(Team, slug=team_slug)
    page.group = team
    page.save()
    action.send(
        request.user,
        verb='moved site-wide wiki page to team',
        action_object=page,
        target=page.group,
    )
    return HttpResponseRedirect(page.get_absolute_url())
