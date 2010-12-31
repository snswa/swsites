from django.db import models

from cms.models import CMSPlugin

from planet.models import Feed


class PostsForFeed(CMSPlugin):

    feed = models.ForeignKey(Feed)
    limit = models.IntegerField(default=10)

    def __unicode__(self):
        return u'Up to {0} posts from {1}'.format(self.limit, self.feed)
