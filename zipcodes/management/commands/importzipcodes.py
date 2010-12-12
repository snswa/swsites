import csv

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from zipcodes.models import ZipCode


class Command(BaseCommand):

    args = '<zipcode-csv-file> [<state>]'
    help = 'Imports ZIP code information from a CSV file'

    def handle(self, *args, **options):
        if len(args) < 1:
            raise CommandError('Specify the CSV file to import from. Download from http://federalgovernmentzipcodes.us/free-zipcode-database.csv')
        csv_filename = args[0]
        if len(args) == 2:
            restrict_to_state = args[1]
        else:
            restrict_to_state = None
        # Start transaction to increase import speed.
        transaction.commit_unless_managed()
        transaction.enter_transaction_management()
        transaction.managed(True)
        # Import the file.
        with open(csv_filename, 'rU') as f:
            reader = csv.DictReader(f)
            for record in reader:
                # Skip records we aren't interested in.
                if (record['Preferred'] == 'No'
                    or record['Country'] != 'US'
                    or record['Decommisioned'] == 'Yes'
                    or (restrict_to_state and record['State'] != restrict_to_state)
                    ):
                    continue
                if ZipCode.objects.filter(zip_code=record['Zipcode']).count() == 0:
                    zip_code = ZipCode(
                        zip_code=record['Zipcode'],
                        lat=record['lat'],
                        long=record['Long'],
                        city=record['City'],
                        state=record['State'],
                        county=record['County'],
                    )
                    zip_code.save()
                    print('* {0}'.format(zip_code))
        # Done.
        transaction.commit()
        transaction.leave_transaction_management()
        print('')
        print('Imported {0} records.'.format(
            ZipCode.objects.all().count(),
        ))
