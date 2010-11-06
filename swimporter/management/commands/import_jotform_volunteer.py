import csv
from datetime import datetime
from json import dumps
from pprint import pprint

from django.conf import settings
from django.contrib.comments.models import Comment
from django.core.management.base import BaseCommand

from swcontacts.models import (
    Address, Change, Email, Interest, Organization, Person, Phone,
    Relationship,
    )


class Command(BaseCommand):
    args = '<input_file>'
    help = 'Import the specified jotform volunteer CSV file'

    def handle(self, *args, **options):
        with open(args[0], 'rU') as f:
            reader = csv.DictReader(f)
            for row in reader:
                #
                # Strip whitespace.
                for key in row.keys():
                    row[key] = row[key].strip()
                #
                # Build submission datetime object.
                submission_date = datetime(
                    int(row['Submission Date'][0:4]),
                    int(row['Submission Date'][5:7]),
                    int(row['Submission Date'][8:10]),
                    int(row['Submission Date'][11:13]),
                    int(row['Submission Date'][14:16]),
                    int(row['Submission Date'][17:]),
                    )
                #
                # Create Person
                person = Person.objects.create(
                    given_name=row['First Name'],
                    surname=row['Last Name'],
                    )
                person.tags.add('jotform', 'volunteer', '2011')
                #
                print 'Importing %s' % person
                #
                # Record import time
                Change.objects.create(
                    contact=person,
                    message='Imported from JotForm',
                    )
                #
                # Record sign-up time
                Change.objects.create(
                    contact=person,
                    timestamp=submission_date,
                    message='Online new volunteer sign-up',
                    )
                #
                # Email.
                Email.objects.create(
                    contact=person,
                    email=row['E-mail'],
                    added=submission_date,
                    )
                #
                # Phone number.
                Phone.objects.create(
                    contact=person,
                    number=row['Phone Number'],
                    added=submission_date,
                    )
                #
                # Build address text and store address.
                address_text = row['Street Address']
                if row['Street Address Line 2']:
                    address_text += '\n' + row['Street Address Line 2']
                address_text += '\n%s, %s %s\n%s' % (
                    row['City'],
                    row['State / Province'],
                    row['Postal / Zip Code'],
                    row['Country'],
                    )
                Address.objects.create(
                    contact=person,
                    address=address_text,
                    postal_code=row['Postal / Zip Code'],
                    added=submission_date,
                    )
                #
                # Separate and record interests.
                interests = row['Interests'].split('<br>')
                for interest in interests:
                    interest_obj, created = Interest.objects.get_or_create(
                        name=interest,
                        )
                    if created:
                        interest_obj.save()
                    person.interests.add(interest_obj)
                    person.save()
                #
                # Record other talents or resources as comments.
                comment = Comment.objects.create(
                    site_id=settings.SITE_ID,
                    content_object=person,
                    user_name='%s %s' % (person.given_name, person.surname),
                    user_email=row['E-mail'],
                    submit_date=submission_date,
                    is_public=True,
                    comment='\n'.join([
                        "Other talents or resources I'd like to offer:",
                        row["Other talents or resources you'd like to offer"],
                        ])
                    )
                #
                # Find or create a union if a union name is given.
                if row['Union Name']:
                    union_name = row['Union Name']
                    if row['Union Local #']:
                        union_name += ' Local ' + row['Union Local #']
                    union, created = Organization.objects.get_or_create(
                        name=union_name,
                        )
                    if created:
                        union.tags.add('union local')
                        union.save()
                        #
                        # Record import time
                        Change.objects.create(
                            contact=union,
                            message='Imported from JotForm',
                            )
                        #
                        # Record sign-up time
                        Change.objects.create(
                            contact=union,
                            timestamp=submission_date,
                            message='Created via online new volunteer sign-up',
                            )
                    #
                    # Record relationship between person and union.
                    Relationship.objects.create(
                        who=person,
                        whom=union,
                        tag='is member of',
                        added=submission_date,
                        )
                    Relationship.objects.create(
                        who=union,
                        whom=person,
                        tag='has member',
                        added=submission_date,
                        )
