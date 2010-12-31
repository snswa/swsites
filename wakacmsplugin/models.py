from django.db import models

from cms.models import CMSPlugin
from teams.models import Team
from wakawaka.models import Revision
from wakacmsplugin import api
from wakacmsplugin.settings import TEAM_SLUG


class WikiPageSnippet(CMSPlugin):

    slug = models.CharField('slug', max_length=255)
    rev = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        if self.content() != u'':
            return '{0}@{1}'.format(self.slug, self.rev or 'latest')
        else:
            return 'WARNING: NO CONTENT - {0}@{1}'.format(self.slug, self.rev or 'latest')

    def content(self):
        return api.snippet_content(self.slug, self.rev)

    def revision(self):
        return api.snippet_revision(self.slug, self.rev)
