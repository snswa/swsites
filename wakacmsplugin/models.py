from django.db import models

from cms.models import CMSPlugin

from wakawaka.models import Revision


class WikiPageSnippet(CMSPlugin):

    slug = models.CharField('slug', max_length=255)
    rev = models.IntegerField()

    def __unicode__(self):
        if self.content() != u'':
            return '{0}@{1}'.format(self.slug, self.rev)
        else:
            return 'WARNING: NO CONTENT - {0}@{1}'.format(self.slug, self.rev)

    def content(self):
        try:
            revision = Revision.objects.filter(
                pk=self.rev,
                page__slug=self.slug,
            )[0]
            content = revision.content
            content = content.split('-BEGINSNIPPET-')[1]
            content = content.split('-ENDSNIPPET-')[0]
            return content
        except IndexError:
            return u''
