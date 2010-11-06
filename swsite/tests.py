"""
Side-wide tests.
"""

from django.test import TestCase


class SiteTests(TestCase):

    urls = 'swsite.urls'

    def test_report_ok(self):
        """
        Calling /deploy_tests/report_ok results in "OK".
        """
        response = self.client.get('/deploy_tests/report_ok')
        self.assertContains(response, 'OK')


#__test__ = {"doctest": """
#Another way to test that 1 + 1 is equal to 2.
#
#>>> 1 + 1 == 2
#True
#"""}

