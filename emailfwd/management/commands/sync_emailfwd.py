from __future__ import print_function

import os
import sys
import xmlrpclib

from django.conf import settings
from django.core.management.base import BaseCommand

from emailfwd.models import ForwardedEmailAddress


class Command(BaseCommand):
    help = 'Sync the email forwarding configuration with WebFaction'

    def handle(self, *args, **options):
        server = xmlrpclib.ServerProxy('https://api.webfaction.com/')
        #
        # Sign in.
        session_id, account = server.login(settings.WEBFACTION_USERNAME, settings.WEBFACTION_PASSWORD)
        #
        # Determine existing email addresses.
        emails = server.list_emails(session_id)
        existing_addresses = dict((info['email_address'], info) for info in emails if info['email_address'][0] not in '@_')
        #
        # Determine desired configuration.
        desired_configuration = {}
        desired_addresses = set()
        #
        for fwd in ForwardedEmailAddress.objects.all():
            name = fwd.name.lower()
            domain = fwd.domain.lower()
            email = '{0}@{1}'.format(name, domain)
            desired_configuration[email] = fwd
            desired_addresses.add(email)
        delete_addresses = set(existing_addresses) - desired_addresses
        create_addresses = desired_addresses - set(existing_addresses)
        update_addresses = desired_addresses - create_addresses
        for address in create_addresses:
            config = desired_configuration[address]
            targets = ','.join(dest.email for dest in config.emaildestination_set.all())
            print('creating email={0} to={1}'.format(address, targets))
            server.create_email(session_id, address, targets)
        for address in update_addresses:
            config = desired_configuration[address]
            targets = ','.join(dest.email for dest in config.emaildestination_set.all())
            if targets != existing_addresses[address]['targets']:
                print('updating email={0} targets={1}'.format(address, targets))
                server.update_email(session_id, address, targets)
        for address in delete_addresses:
            print('deleting email={0}'.format(address))
            server.delete_email(session_id, address)
