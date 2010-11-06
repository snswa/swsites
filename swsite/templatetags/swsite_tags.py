import re
from django.core.exceptions import ObjectDoesNotExist
from django.template import Library
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from wakawaka.models import WikiPage

register = Library()


CREOLE_WIKILINK_REGEX = r'\[\[(!\]*)\]\]'
CREOLE_WIKILINK_REGEX = re.compile(CREOLE_WIKILINK_REGEX)


def replace_wikilinks(value, exists_template, missing_template):
    def replace_wikiword(m):
        slug = m.group(1)
        parts = slug.split('|', 1)
        if not parts:
            # empty link
            return ''
        if len(parts) == 1:
            slug = text = parts[0]
        else:
            slug, text = parts
        slug = slug.strip()
        text = text.strip()
        if ':' in slug or slug.startswith('.') or slug.startswith('/'):
            # slug is an URL.
            return exists_template.format(url=slug, text=text)
        kwargs = dict(slug=slug)
        try:
            page = WikiPage.objects.get(slug=slug)
        except ObjectDoesNotExist:
            url = reverse('wakawaka_edit', kwargs=kwargs)
            return missing_template.format(url=url, text=text)
        else:
            url = reverse('wakawaka_page', kwargs=kwargs)
            return exists_template.format(url=url, text=text)
    return mark_safe(CREOLE_WIKILINK_REGEX.sub(replace_wikiword, value))


@register.filter
def wikify_creole_links(value):
    """Turns [[Wiki Links]] into [[Wiki Links|full-url-to-page]]"""
    return replace_wikilinks(
        value,
        exists_template=r'[[{url:>s}|{text:>s}]]',
        missing_template=r'[[{url:>s}|{text:>s}?]]',
        )
