from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from wakawaka.models import Revision

from wakacmsplugin.models import WikiPageSnippet


class WikiPageSnippetPlugin(CMSPluginBase):

    model = WikiPageSnippet
    name = _("Wiki Page Snippet")
    render_template = "wakacmsplugin/wikipagesnippet.html"

    def render(self, context, instance, placeholder):
        content = instance.content()
        context.update({
            'content': content,
            'placeholder': placeholder,
        })
        return context


plugin_pool.register_plugin(WikiPageSnippetPlugin)
