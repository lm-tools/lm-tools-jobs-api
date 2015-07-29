from django.test import TestCase

from jobs_api.adzuna import Adzuna
from jobs.models import JobArea


class TestAdzunaLib(TestCase):

    def test_jobs_at_location(self):
        az = Adzuna()
        x = az.jobs_at_location('UK', 'London', 'South East London', 15)
        self.assertEqual(len(x), 15)

    def test_top_companies(self):
        az = Adzuna()
        x = az.top_companies('UK', 'London', 'South East London', 2)
        self.assertEqual(len(x), 2)

    def test_locations_for_invalid_postcode(self):
        az = Adzuna()
        self.assertRaises(
            AssertionError,
            az.locations_for_postcode, 'not a postcode'
        )

    def test_locations_for_valid_postcode(self):
        az = Adzuna()
        x = az.locations_for_postcode('SW1H0ET')
        self.assertEqual(len(x), 3)
