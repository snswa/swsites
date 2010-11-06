import csv
from datetime import datetime
from json import dumps
from pprint import pprint

from django.core.management.base import BaseCommand

from roster.models import Person, Change, Address, Phone, Email
from fundraiser.models import Donation


class Command(BaseCommand):
    args = '<input_file>'
    help = 'Import the specified jotform donation CSV file'

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
                # Find donation amount.
                parts = row['Donation'].split('<br>')
                for part in parts:
                    if part.startswith('Total'):
                        donation_amount = int(part.split('$')[1])
                        break
                #
                # Create Person
                person = Person.objects.create(
                    given_name=row['First Name'],
                    surname=row['Last Name'],
                    )
                person.tags.add('jotform', 'donor', '2011')
                #
                print 'Importing %s' % person
                #
                # Record import time
                Change.objects.create(
                    contact=person,
                    message='Imported from JotForm',
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
                # Phone number.
                Phone.objects.create(
                    contact=person,
                    number=row['Phone Number'],
                    added=submission_date,
                    )
                #
                # Email.
                Email.objects.create(
                    contact=person,
                    email=row['E-mail'],
                    added=submission_date,
                    )
                #
                # Record donation time
                change = Change.objects.create(
                    contact=person,
                    timestamp=submission_date,
                    message='Online donation',
                    )
                #
                # Compliance information.
                compliance_information = dict(
                    occupation=row['Occupation'],
                    employer=row['Employer'],
                    compliance_statement=True,
                    )
                Donation.objects.create(
                    contact=person,
                    amount=donation_amount,
                    payment_method='PayPal',
                    compliance_information=dumps(compliance_information),
                    timestamp=submission_date,
                    )
