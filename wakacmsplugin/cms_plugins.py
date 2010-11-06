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
        #
        # Get the actual wiki page and strip everything but the content block.
        try:
            revision = Revision.objects.filter(
                pk=instance.rev,
                page__slug=instance.slug,
            )[0]
            content = revision.content
            content = content.split('-BEGINSNIPPET-')[1]
            content = content.split('-ENDSNIPPET-')[0]
        except IndexError:
            raise ValueError(
                'No content snippet found at %s:%s'
                % (instance.slug, instance.rev)
            )
        #
        context.update({
            'content': content,
            'placeholder': placeholder,
        })
        return context


plugin_pool.register_plugin(WikiPageSnippetPlugin)
