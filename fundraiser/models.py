import django.db.models as m
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from taggit.managers import TaggableManager


class Donation(m.Model):
    """Record of a donation.

    `compliance_information` is a JSON-structured dictionary of information
    needed when producing compliance reports, e.g.::

        { "occupation": ...
        , "employer": ...
        , "compliance_statement": True
        }
    """

    PAYMENT_METHOD_CHOICES = [
        ('CC', 'Credit Card'),
        ('PayPal', 'PayPal'),
        ('Check', 'Check'),
        ('Cash', 'Cash'),
        ]

    content_type = m.ForeignKey(ContentType)
    object_id = m.PositiveIntegerField()
    contact = generic.GenericForeignKey('content_type', 'object_id')

    amount = m.DecimalField(max_digits=10, decimal_places=2)
    payment_method = m.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    compliance_information = m.TextField()
    timestamp = m.DateTimeField(auto_now_add=True)
