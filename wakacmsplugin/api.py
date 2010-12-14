import re

from teams.models import Team
from wakawaka.models import Revision
from wakacmsplugin.settings import TEAM_SLUG


SNIPPET_RE = re.compile(r'.*-BEGINSNIPPET-\W+(.*)\W+-ENDSNIPPET-.*', re.DOTALL)


def latest_rev_id(slug):
    return snippet_revision(slug, None).id


def snippet_content(slug, rev_id):
    rev = snippet_revision(slug, rev_id)
    if rev is None:
        return u''
    else:
        content = rev.content
        match = SNIPPET_RE.match(content)
        if match:
            return match.group(1)
        else:
            return '(WARNING: No content snippet found)'


def snippet_revision(slug, rev_id):
    try:
        if TEAM_SLUG is None:
            queryset = Revision.objects.filter(
                page__content_type=None,
                page__object_id=None,
            )
        else:
            team = Team.objects.get(slug=TEAM_SLUG)
            queryset = team.content_objects(Revision, join='page')
        if rev_id:
            revision = queryset.get(
                pk=rev_id,
                page__slug=slug,
            )
        else:
            revision = queryset.filter(page__slug=slug).latest('modified')
        return revision
    except (IndexError, Revision.DoesNotExist):
        return None
