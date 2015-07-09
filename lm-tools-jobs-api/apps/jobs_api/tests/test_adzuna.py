from django.test import TestCase

from jobs_api.adzuna import Adzuna

class TestAdzunaLib(TestCase):

    def test_jobs_at_location(self):
        az = Adzuna()
        x = az.jobs_at_location('UK', 'London', 'South East London', 15)
        self.assertEqual(len(x), 15)

    def test_top_companies(self):
         az = Adzuna()
         x = az.top_companies('UK', 'London', 'South East London', 2)
         self.assertEqual(len(x), 2)
