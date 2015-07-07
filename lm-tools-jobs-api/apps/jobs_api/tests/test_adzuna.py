from django.test import TestCase

from jobs_api.adzuna import Adzuna

class TestAdzunaLib(TestCase):

    def test_jobs_at_location(self):
        az = Adzuna()
        x = az.jobs_at_loation('UK', 'London', 'South East London')
        self.assertEqual(x.status_code, 200)