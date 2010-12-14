import re

from teams.models import Team
from wakacmsplugin.api import latest_rev_id, snippet_content
from wakacmsplugin.models import WikiPageSnippet
from wakacmsplugin.settings import TEAM_SLUG


REV_CODE_RE = re.compile(r'$r([0-9]+)^')


def wakacms_snippets(request):
    """Usage:  wakacms_snippets.SlugName.latest or wakacms_snippets.SlugName.r123"""
    try:
        snippetgroup = Team.objects.get(slug=TEAM_SLUG)
    except Team.DoesNotExist:
        snippetgroup = None
    return {
        'wakacms_snippets': WakaCmsSnippets(),
        'wakacms_snippetgroup': snippetgroup,
    }


class WakaCmsSnippets(object):

    def __getitem__(self, slug):
        return Snippet(slug)


class Snippet(object):

    def __init__(self, slug):
        self.slug = slug

    def __getitem__(self, rev_code):
        rev = None
        if rev_code == 'latest':
            rev = latest_rev_id(self.slug)
        else:
            match = REV_CODE_RE.match(rev_code)
            if match:
                rev = int(match[1])
        if rev:
            # an ephemeral snippet instance, never saved
            return WikiPageSnippet(slug=self.slug, rev=rev)
