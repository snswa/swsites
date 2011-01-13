import re

from django.core.exceptions import ObjectDoesNotExist
from django.template import Library, Node, Variable
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from actstream.models import Action
from relationships.utils import relationship_exists
from wakawaka.models import WikiPage


register = Library()


# --- WIKI LINKS ---


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
        if ':' in slug or '#' in slug or slug.startswith('.') or slug.startswith('/'):
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


@register.filter
def canviewwikipage(user, page):
    return user.has_perm('wakawaka.can_view', page)

@register.filter
def canresetwikieditlockingroup(user, group):
    return user.has_perm('wakawaka.reset_lock', group)

@register.filter
def candeletewikipage(user, page):
    return user.has_perm('wakawaka.delete_wikipage', page)

@register.filter
def canchangewikipage(user, page):
    return user.has_perm('wakawaka.change_wikipage', page)

@register.filter
def canaddwikipagetogroup(user, group):
    return user.has_perm('wakawaka.add_wikipage', group)


# --- PROFILE PRIVACY ---


def _is_coordinator(u, o):
    coordinator_teams = set(m.team for m in u.member_set.filter(is_coordinator=True))
    other_teams = set(o.team_set.all())
    if other_teams.intersection(coordinator_teams):
        return True
    else:
        return False

_privacy_conditions = {
    # privacy-code: lookup-fn,
    'P': lambda u, o: False,
    'C': lambda u, o: _is_coordinator(u, o),
    'F': lambda u, o: _is_coordinator(u, o) or relationship_exists(o, u, 'following'),
    'A': lambda u, o: True,
}

for _section in [
    'name',
    'zip_code',
    'mailing_address',
    'email',
    'phone_number',
    'messaging',
    'preferred_contact_methods',
    'bio',
    'occupation',
    'employer',
    ]:
    def canview_x_ofuser(user, other, _section=_section):
        if user == other:
            return True
        # Check other user's profile for their privacy setting.
        other_profile = other.get_profile()
        privacy_name = '{0}_privacy'.format(_section)
        privacy_code = getattr(other_profile, privacy_name)
        # Determine the privacy condition based on their setting.
        return _privacy_conditions[privacy_code](user, other)
    _name = canview_x_ofuser.__name__ = 'canview_{0}_ofuser'.format(_section)
    globals()[_name] = register.filter(canview_x_ofuser)


@register.tag
def profile_privacy(parser, token):
    """Determine profile visibility based on the the profile's privacy settings
    and the current user's relationship to the profile's user.

    Example::

        <% load sw_tags %>
        <% profile_privacy %>

    Assumes the context contains 'user' and 'profile'.
    """
    return ProfilePrivacyNode()


class ProfilePrivacyNode(Node):

    def render(self, context):
        # Determine if user is a coordinator of one of other's teams.
        user = context['user']
        profile = context['profile']
        other = profile.user
        #
        is_me = context['is_me']
        #
        # Determine if current user is a coordinator of a team that the other user is a member of.
        coordinator_teams = set(m.team for m in user.member_set.filter(is_coordinator=True))
        other_teams = set(other.team_set.all())
        if other_teams.intersection(coordinator_teams):
            is_coordinator = True
        else:
            is_coordinator = False
        #
        # Determine if the other user follows the current user.
        is_friend = relationship_exists(other, user, 'following')
        #
        # Now determine privacy settings for each section.
        privacy_conditions = {
            # privacy-code: lookup-fn,
            'P': False,
            'C': is_coordinator,
            'F': is_coordinator or is_friend,
            'A': True,
        }
        for section in [
            'name',
            'zip_code',
            'interests',
            'bio',
            'email',
            'phone_number',
            'messaging',
            'mailing_address',
            'preferred_contact_methods',
            'occupation',
            'employer',
            'union',
            ]:
            privacy_name = '{0}_privacy'.format(section)
            privacy_code = getattr(profile, privacy_name)
            context['can_view_{0}'.format(section)] = is_me or privacy_conditions[privacy_code]
            if privacy_code != 'A':
                context['{0}_restricted'.format(section)] = True
        return u''


# --- ACTIONS ---

@register.filter
def teamactions(team, limit=None):
    queryset = team.content_objects(Action, gfk_field='target').order_by('-timestamp')
    if limit is not None:
        queryset = queryset[:limit]
    return queryset
