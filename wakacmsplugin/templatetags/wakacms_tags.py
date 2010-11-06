from django import template

from wakawaka.models import WikiPage
from wakacmsplugin.models import WikiPageSnippet

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
