import re
from django.core.exceptions import ObjectDoesNotExist
from django.template import Library, Node, Variable
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from wakawaka.models import WikiPage

register = Library()


CREOLE_WIKILINK_REGEX = r'\[\[([^\]]*)\]\]'
CREOLE_WIKILINK_REGEX = re.compile(CREOLE_WIKILINK_REGEX)


def replace_wikilinks(value, group, exists_template, missing_template):
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
        # See if the page exists.
        if group:
            queryset = group.content_objects(WikiPage)
        else:
            queryset = WikiPage.objects.filter(content_type=None, object_id=None)
        page_exists = (queryset.filter(slug=slug).count() == 1)
        # Create view or edit URL accordingly.
        if page_exists:
            if group:
                url = group.content_bridge.reverse('wakawaka_page', group, kwargs=kwargs)
            else:
                url = reverse('wakawaka_page', kwargs=kwargs)
            return exists_template.format(url=url, text=text)
        else:
            if group:
                url = group.content_bridge.reverse('wakawaka_edit', group, kwargs=kwargs)
            else:
                url = reverse('wakawaka_edit', kwargs=kwargs)
            return missing_template.format(url=url, text=text)
    return mark_safe(CREOLE_WIKILINK_REGEX.sub(replace_wikiword, value))


@register.filter
def wikify_creole_links(value, group):
    """Turns [[Wiki Links]] into [[Wiki Links|full-url-to-page]]"""
    return replace_wikilinks(
        value,
        group,
        exists_template=r'[[{url:>s}|{text:>s}]]',
        missing_template=r'[[{url:>s}|{text:>s}?]]',
        )
#
#
# class WikifyCreoleContentNode(Node):
#
#     def __init__(self, content_expr, group_var):
#         self.content_expr = content_expr
#         self.group_var = Variable(group_var)
#
#     def render(self, context):
#         content = self.content_expr.resolve(context)
#         group = self.group_var.resolve(context)
#         return replace_wikilinks(content, group)
#
#
# @register.tag
# def wikify_creole_content(parser, token):
#     bits = token.split_contents()
#     try:
#         group_var = bits[2]
#     except IndexError:
#         group_var = None
#     return WikifyCreoleContentNode(parser.compile_filter(bits[1]), group_var)
