from __future__ import print_function

import os
import sys

from django.core.management.base import BaseCommand

from emailfwd.models import ForwardedEmailAddress


class Command(BaseCommand):
    args = '<output_dir>'
    help = 'Export the email forwarding data directory'

    def handle(self, *args, **options):
        output_dir = args[0]
        if not os.path.isdir(output_dir) or os.listdir(output_dir):
            print('Provide an empty directory that exists', file=sys.stderr)
            return 1
        for fwd in ForwardedEmailAddress.objects.all():
            name = fwd.name.lower()
            domain = fwd.domain.lower()
            outname = os.path.join(output_dir, '{0}@{1}'.format(name, domain))
            with open(outname, 'wb') as out:
                for dest in fwd.emaildestination_set.all():
                    print(dest.email.lower(), file=out)
