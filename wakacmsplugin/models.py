from django.db import models

from cms.models import CMSPlugin


class WikiPageSnippet(CMSPlugin):

    slug = models.CharField('slug', max_length=255)
    rev = models.IntegerField()

    def __unicode__(self):
        return '%s @ %s' % (self.slug, self.rev)
