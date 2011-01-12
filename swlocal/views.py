from operator import attrgetter

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext

from swlocal.models import teams_for_zip_code


@login_required
def index(request):
    if not request.features['local']:
        return HttpResponseRedirect(reverse('sw_placeholder', kwargs=dict(slug='local')))
    template_name = 'local/index.html'
    regional_teams = teams_for_zip_code(request.user.get_profile().zip_code)
    for team in regional_teams:
        team.coordinators = team.members.filter(member__is_coordinator=True)
    #
    template_context = {
        'regional_teams': sorted(regional_teams, key=attrgetter('name')),
    }
    return render_to_response(template_name, template_context, RequestContext(request))
