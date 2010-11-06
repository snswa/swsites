import django.db.models as m
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from taggit.managers import TaggableManager


class Person(m.Model):
    """An individual person."""

    given_name = m.CharField(max_length=50, null=True)
    middle_name = m.CharField(max_length=50, null=True)
    surname = m.CharField(max_length=50, null=True)
    last_contacted = m.DateTimeField(null=True)
    interests = m.ManyToManyField('Interest')
    tags = TaggableManager()

    def __unicode__(self):
        return '%s %s' % (self.given_name, self.surname)


class Organization(m.Model):
    """A group of people acting in an organization."""

    name = m.CharField(max_length=200, null=True)
    last_contacted = m.DateTimeField(null=True)
    tags = TaggableManager()

    def __unicode__(self):
        return self.name


class Change(m.Model):

    # Link to either a person or an organization.
    content_type = m.ForeignKey(ContentType)
    object_id = m.PositiveIntegerField()
    contact = generic.GenericForeignKey('content_type', 'object_id')

    user = m.ForeignKey("auth.User", null=True)
    timestamp = m.DateTimeField(auto_now_add=True)
    message = m.CharField(max_length=250)


class Address(m.Model):

    TYPE_CHOICES = [
        ('M', 'Mailing'),
        ('H', 'Home'),
        ('B', 'Business'),
        ]

    # Link to either a person or an organization.
    content_type = m.ForeignKey(ContentType)
    object_id = m.PositiveIntegerField()
    contact = generic.GenericForeignKey('content_type', 'object_id')

    type = m.CharField(max_length=1, choices=TYPE_CHOICES, null=True)
    address = m.TextField()
    postal_code = m.CharField(max_length=20, null=True)
    added = m.DateTimeField(auto_now_add=True)


class Phone(m.Model):

    TYPE_CHOICES = [
        ('H', 'Home'),
        ('W', 'Work'),
        ('M', 'Mobile'),
        ]

    # Link to either a person or an organization.
    content_type = m.ForeignKey(ContentType)
    object_id = m.PositiveIntegerField()
    contact = generic.GenericForeignKey('content_type', 'object_id')

    type = m.CharField(max_length=1, choices=TYPE_CHOICES, null=True)
    number = m.CharField(max_length=50)
    added = m.DateTimeField(auto_now_add=True)
    validated = m.DateTimeField(null=True)


class Email(m.Model):

    TYPE_CHOICES = [
        ('P', 'Personal'),
        ('W', 'Work'),
        ]

    # Link to either a person or an organization.
    content_type = m.ForeignKey(ContentType)
    object_id = m.PositiveIntegerField()
    contact = generic.GenericForeignKey('content_type', 'object_id')

    email = m.EmailField()
    type = m.CharField(max_length=1, choices=TYPE_CHOICES, null=True)
    added = m.DateTimeField(auto_now_add=True)
    validated = m.DateTimeField(null=True)


class Relationship(m.Model):

    # Link to either a person or an organization.
    who_content_type = m.ForeignKey(ContentType, related_name='relationship_who_set')
    who_object_id = m.PositiveIntegerField()
    who = generic.GenericForeignKey('who_content_type', 'who_object_id')

    # Link to either a person or an organization.
    whom_content_type = m.ForeignKey(ContentType, related_name='relationship_whom_set')
    whom_object_id = m.PositiveIntegerField()
    whom = generic.GenericForeignKey('whom_content_type', 'whom_object_id')

    tag = m.CharField(max_length=50)
    added = m.DateTimeField(auto_now_add=True)


class Interest(m.Model):

    name = m.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name
