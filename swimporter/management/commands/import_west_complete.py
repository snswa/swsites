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
                    if row[key]:
                        row[key] = row[key].strip()
                    else:
                        row[key] = ''
                #
                # Create Person
                if row['fname'] and row['lname']:
                    person = Person.objects.create(
                        given_name=row['fname'],
                        surname=row['lname'],
                        )
                elif row['fullname']:
                    person = Person.objects.create(
                        given_name=row['fullname'],
                        )
                person.tags.add('west complete', 'volunteer', '2010')
                person.save()
                #
                print 'Importing %s' % person
                #
                # Build submission datetime object.
                parts = row['Add Date'].split('/')
                if len(parts) == 3:
                    if len(parts[2]) == 2:
                        year = '20' + parts[2]
                    elif len(parts[2]) == 4:
                        year = parts[2]
                    submission_date = datetime(
                        int(year),
                        int(parts[0]),
                        int(parts[1]),
                        )
                else:
                    submission_date = datetime.now()
                    Change.objects.create(
                        contact=person,
                        message='Note: Add date not given in West Complete.',
                        )
                #
                # Record import time
                Change.objects.create(
                    contact=person,
                    message='Imported from West Complete',
                    )
                #
                # Form address.
                address_lines = []
                if row['ADDRESS']:
                    address_lines.append(row['ADDRESS'])
                if row['CITY']:
                    address_lines.append(
                        '%s, WA %s' % (row['CITY'], row['ZIP']))
                if row['COUNTY']:
                    address_lines.append('%s county' % row['COUNTY'])
                Address.objects.create(
                    contact=person,
                    address='\n'.join(address_lines),
                    postal_code=row['ZIP'],
                    added=submission_date,
                    )
                #
                # Phone number.
                if row['PHONE']:
                    Phone.objects.create(
                        contact=person,
                        number=row['PHONE'],
                        added=submission_date,
                        )
                #
                # Email.
                if row['email']:
                    first_email = None
                    emails = row['email'].split(',')
                    for email in emails:
                        email = email.strip()
                        if not first_email:
                            first_email = email
                        Email.objects.create(
                            contact=person,
                            email=email,
                            added=submission_date,
                            )
                #
                # Notes.
                comment = Comment.objects.create(
                    site_id=settings.SITE_ID,
                    content_object=person,
                    user_name='%s %s' % (person.given_name, person.surname),
                    user_email=first_email,
                    submit_date=submission_date,
                    is_public=True,
                    comment=row['NOTES'],
                    )
