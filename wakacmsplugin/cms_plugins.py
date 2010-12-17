from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from wakawaka.models import Revision

from wakacmsplugin.models import WikiPageSnippet
from wakacmsplugin.settings import TEAM_SLUG

from teams.models import Team


class WikiPageSnippetPlugin(CMSPluginBase):

    model = WikiPageSnippet
    name = _("Wiki Page Snippet")
    render_template = "wakacmsplugin/wikipagesnippet.html"

    def render(self, context, instance, placeholder):
        try:
            snippetgroup = Team.objects.get(slug=TEAM_SLUG)
        except Team.DoesNotExist:
            snippetgroup = None
        content = instance.content()
        context.update({
            'snippet': instance,
            'placeholder': placeholder,
            'wakacms_snippetgroup': snippetgroup,
            'slug': instance.slug,
            'rev_id': instance.rev,
        })
        return context


plugin_pool.register_plugin(WikiPageSnippetPlugin)
