from operator import attrgetter

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext

from zipcodes.models import County, ZipCode


@login_required
def index(request):
    if not request.features['local']:
        return HttpResponseRedirect(reverse('sw_placeholder', kwargs=dict(slug='local')))
    template_name = 'local/index.html'
    #
    # Find regional teams for the user.
    regional_teams = set()
    # First look for teams directly in the user's ZIP code.
    zip_code = request.user.get_profile().zip_code
    try:
        zip_code = ZipCode.objects.get(zip_code=zip_code)
    except ZipCode.DoesNotExist:
        pass
    else:
        regional_teams.update(zip_code.teams.all())
        # Also look for teams that match the ZIP code's county.
        county = County.objects.get(name=zip_code.county)
        regional_teams.update(county.teams.all())
    for team in regional_teams:
        team.coordinators = team.members.filter(member__is_coordinator=True)
    #
    template_context = {
        'regional_teams': sorted(regional_teams, key=attrgetter('name')),
    }
    return render_to_response(template_name, template_context, RequestContext(request))
