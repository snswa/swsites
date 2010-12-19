import re
from django.core.exceptions import ObjectDoesNotExist
from django.template import Library, Node, Variable
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
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


# --- PROFILE PRIVACY ---


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
        is_me = context['is_me']
        coordinator_teams = set(m.team for m in user.member_set.filter(is_coordinator=True))
        other_teams = set(other.team_set.all())
        if other_teams.intersection(coordinator_teams):
            is_coordinator = True
        else:
            is_coordinator = False
        # TODO: Find out
        # Now determine privacy settings for each section.
        privacy_map = {
            # privacy-code: lookup-fn,
            'P': False,
            'C': is_coordinator,
            'F': is_coordinator,
            'A': True,
        }
        for section in [
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
            privacy_name = '{0}_privacy'.format(section)
            privacy_code = getattr(profile, privacy_name)
            context['can_view_{0}'.format(section)] = is_me or privacy_map[privacy_code]
            if privacy_code != 'A':
                context['{0}_restricted'.format(section)] = True
        return u''
