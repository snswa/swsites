from django import template

from teams.models import Team

from wakawaka.models import WikiPage

from wakacmsplugin.api import latest_rev_id, snippet_content
from wakacmsplugin.models import WikiPageSnippet
from wakacmsplugin.settings import TEAM_SLUG


register = template.Library()


@register.inclusion_tag('wakacmsplugin/tags/related_cms_pages.html',
                        takes_context=True)
def related_cms_pages(context):
    wiki_page = context['page']
    wiki_snippets = WikiPageSnippet.objects.filter(slug=wiki_page.slug).all()
    snippet_pages = []
    for snippet in wiki_snippets:
        for page in snippet.placeholder.page_set.all():
            snippet_pages.append({
                'snippet': snippet,
                'page': page,
            })
    return {
        'snippet_pages': snippet_pages,
    }


@register.tag
def wikipagesnippet(parser, token):
    """Includes a wiki page snippet on the current page.

    Examples:

        {% wikipagesnippet DashboardPreamble latest %}  {# Latest rev. #}
        {% wikipagesnippet DashboardPreamble 1029 %}    {# Specific rev. #}
    """
    tag_name, slug, rev_id = token.split_contents()
    if rev_id == 'latest':
        rev_id = None
    else:
        rev_id = int(rev_id)
    return WikiPageSnippetNode(slug, rev_id)


class WikiPageSnippetNode(template.Node):

    def __init__(self, slug, rev_id):
        self.slug = slug
        self.rev_id = rev_id

    def render(self, context):
        try:
            snippetgroup = Team.objects.get(slug=TEAM_SLUG)
        except Team.DoesNotExist:
            snippetgroup = None
        t = template.loader.get_template('wakacmsplugin/wikipagesnippet.html')
        # an ephemeral snippet instance, never saved
        if self.rev_id is None:
            rev_id = latest_rev_id(self.slug)
        else:
            rev_id = self.rev_id
        snippet = WikiPageSnippet(slug=self.slug, rev=rev_id)
        context = template.Context({
            'is_wakacms_team_member': context['is_wakacms_team_member'],
            'slug': self.slug,
            'rev_id': self.rev_id,
            'snippet': snippet,
            'wakacms_snippetgroup': snippetgroup,
        }, autoescape=context.autoescape)
        return t.render(context)
