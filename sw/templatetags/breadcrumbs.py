# http://djangosnippets.org/snippets/1289/

from django import template
from django.template import loader, Node, Variable
from django.utils.encoding import smart_str, smart_unicode
from django.template.defaulttags import url
from django.template import VariableDoesNotExist

register = template.Library()

@register.tag
def breadcrumb(parser, token):
    """
    Renders the breadcrumb.
    Examples:
        {% breadcrumb "Title of breadcrumb" url_var %}
        {% breadcrumb context_var  url_var %}
        {% breadcrumb "Just the title" %}
        {% breadcrumb just_context_var %}

    Parameters:
    -First parameter is the title of the crumb,
    -Second (optional) parameter is the url variable to link to, produced by url tag, i.e.:
        {% url person_detail object.id as person_url %}
        then:
        {% breadcrumb person.name person_url %}

    @author Andriy Drozdyuk
    """
    bits = token.split_contents()
    # Insert empty CSS class.
    bits.insert(1, '""')
    token.contents = ' '.join(bits)
    bits = token.split_contents()[1:]
    return BreadcrumbNode(bits)


@register.tag
def breadcrumb_css(parser, token):
    """Same as breadcrumb, except specify a CSS class in front."""
    bits = token.split_contents()[1:]
    return BreadcrumbNode(bits)


@register.tag
def breadcrumb_url(parser, token, css_class='""'):
    """
    Same as breadcrumb
    but instead of url context variable takes in all the
    arguments URL tag takes.
        {% breadcrumb "Title of breadcrumb" person_detail person.id %}
        {% breadcrumb person.name person_detail person.id %}
    """

    bits = token.split_contents()
    if len(bits)==2:
        return breadcrumb(parser, token)

    # Extract our extra title parameter
    title = bits.pop(1)
    token.contents = ' '.join(bits)
    # Shove it back into to the token to url parse it.
    url_node = url(parser, token)

    return UrlBreadcrumbNode(css_class, title, url_node)


@register.tag
def breadcrumb_url_css(parser, token):
    """Same as breadcrumb_url, except specify a CSS class in front."""
    bits = token.split_contents()
    css_class = bits.pop(1)
    print 'css_class', css_class, 'bits', bits
    token.contents = ' '.join(bits)
    return breadcrumb_url(parser, token, css_class)


class BreadcrumbNode(Node):
    def __init__(self, vars):
        self.vars = map(Variable,vars)
        # 0 -> css class
        # 1 -> title
        # 2 -> url

    def render(self, context):
        css_class = self.vars[0].var
        if css_class.find("'") == -1 and css_class.find('"') == -1:
            try:
                val = self.vars[0]
                css_class = val.resolve(context)
            except:
                css_class = ''
        else:
            css_class = css_class.strip("'").strip('"')
            css_class = smart_unicode(css_class)
        #
        title = self.vars[1].var
        if title.find("'") == -1 and title.find('"') == -1:
            try:
                val = self.vars[1]
                title = val.resolve(context)
            except:
                title = ''
        else:
            title = title.strip("'").strip('"')
            title = smart_unicode(title)
        #
        url = None
        if len(self.vars)>2:
            val = self.vars[2]
            try:
                url = val.resolve(context)
            except VariableDoesNotExist:
                print 'URL does not exist', val
                url = None
        #
        return create_crumb(css_class, title, url)


class UrlBreadcrumbNode(Node):
    def __init__(self, css_class, title, url_node):
        self.css_class = Variable(css_class)
        self.title = Variable(title)
        self.url_node = url_node

    def render(self, context):
        title = self.title.var
        if title.find("'") == -1 and title.find('"') == -1:
            try:
                val = self.title
                title = val.resolve(context)
            except:
                title = ''
        else:
            title = title.strip("'").strip('"')
            title = smart_unicode(title)
        #
        css_class = self.css_class.var
        if css_class.find("'") == -1 and css_class.find('"') == -1:
            try:
                val = self.css_class
                css_class = val.resolve(context)
            except:
                css_class = ''
        else:
            css_class = css_class.strip("'").strip('"')
            css_class = smart_unicode(css_class)
        #
        url = self.url_node.render(context)
        return create_crumb(css_class, title, url)


def create_crumb(css_class, title, url):
    """
    Helper function
    """
    if url:
        crumb = "<li><span class='{css_class}'><a href='{url}'><span>{title}</span></a></span></li>".format(**locals())
    else:
        crumb = "<li><span class='{css_class}'><span>{title}</span></span></li>".format(**locals())

    return crumb
