from django.db import models

from cms.models import CMSPlugin

from teams.models import Team

from wakawaka.models import Revision

from wakacmsplugin.settings import TEAM_SLUG


class WikiPageSnippet(CMSPlugin):

    slug = models.CharField('slug', max_length=255)
    rev = models.IntegerField()

    def __unicode__(self):
        if self.content() != u'':
            return '{0}@{1}'.format(self.slug, self.rev)
        else:
            return 'WARNING: NO CONTENT - {0}@{1}'.format(self.slug, self.rev)

    def content(self):
        revision = self.revision()
        if revision is None:
            return u''
        else:
            content = revision.content
            content = content.split('-BEGINSNIPPET-')[1]
            content = content.split('-ENDSNIPPET-')[0]
            return content

    def revision(self):
        try:
            if TEAM_SLUG is None:
                queryset = Revision.objects.filter(
                    page__content_type=None,
                    page__object_id=None,
                )
            else:
                team = Team.objects.get(slug=TEAM_SLUG)
                queryset = team.content_objects(Revision, join='page')
            revision = queryset.get(
                pk=self.rev,
                page__slug=self.slug,
            )
            return revision
        except (IndexError, Revision.DoesNotExist):
            return None
