from django.test import TestCase

from jobs.models import JobAdvert

class ModelSmokeTests(TestCase):

    def test_str(self):
        ja = JobAdvert(title="Test")
        ja.save()
        self.assertEqual(str(ja), "Unknown (Test)")
