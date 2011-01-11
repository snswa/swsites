import iris.views
from teams.models import Team


def activity(request, slug, *args, **kw):
    template_name = 'teams/activity.html'
    team = get_object_or_404(Team, slug=slug)
    template_context = {
        'group': team,
    }
    return render_to_response(template_name, template_context, RequestContext(request))


def topics(*args, **kwargs):
    # Insert the team into the template context as 'group' so that
    # breadcrumbs, etc. render properly.
    slug = kwargs['slug']
    extra_context = kwargs.setdefault('extra_context', {})
    extra_context['group'] = Team.objects.get(slug=slug)
    return iris.views.topics(*args, **kwargs)
