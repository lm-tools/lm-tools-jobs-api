from django.test import TestCase

from jobs.models import JobAdvert


class TestViews(TestCase):

    def test_travel_time(self):
        ja = JobAdvert(
            title="Test",
            location_text="Diss, Norfolk",
            job_centre_label="sutton"
        )

        self.assertTrue(ja.calculate_travelling_time() > 90)

        ja = JobAdvert(
            title="Test",
            location_text="SM1 1PX",
            job_centre_label="sutton"
        )

        self.assertTrue(ja.calculate_travelling_time() < 90)

        ja = JobAdvert(
            title="Test",
            location_text="ASDASDASDASDASDASDASDADASDAD",
            job_centre_label="sutton"
        )

        self.assertEqual(ja.calculate_travelling_time(), -1)
