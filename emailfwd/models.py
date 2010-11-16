from django.db import models as m

from emailfwd import settings


class ForwardedEmailAddress(m.Model):

    name = m.CharField(max_length=50)
    domain = m.CharField(max_length=50, choices=settings.VALID_DOMAINS, default=settings.DEFAULT_DOMAIN)

    def __unicode__(self):
        destination_count = self.emaildestination_set.count()
        return u'{0.name}@{0.domain} -> {1} address{2}'.format(
            self,
            destination_count,
            'es' if destination_count > 1 else '',
        )


class EmailDestination(m.Model):

    forwarded = m.ForeignKey('ForwardedEmailAddress')
    email = m.EmailField()

    def __unicode__(self):
        return u'{0.name}@{0.domain} -> {1.email}'.format(
            self.forwarded,
            self,
        )
