"""
Side-wide tests.
"""

from django.test import TestCase


class SiteTests(TestCase):

    urls = 'sw.urls'

    def test_report_ok(self):
        """
        Calling /deploy_tests/report_ok results in "OK".
        """
        response = self.client.get('/deploy_tests/report_ok')
        self.assertContains(response, 'OK')
