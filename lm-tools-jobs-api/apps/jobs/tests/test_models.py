from django.test import TestCase

from jobs.models import JobAdvert, JobArea


class ModelSmokeTests(TestCase):

    def test_str(self):
        area = JobArea(locations=["a", "b", "c"])
        area.save()
        ja = JobAdvert(title="Test", job_area=area)
        ja.save()
        self.assertEqual(str(ja), "Unknown (Test)")
