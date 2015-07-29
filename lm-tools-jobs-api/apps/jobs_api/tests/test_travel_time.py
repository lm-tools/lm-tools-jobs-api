from django.test import TestCase

from jobs.models import JobAdvert, JobArea


class TestViews(TestCase):

    def test_travel_time(self):
        area = JobArea(
            locations=["UK", "London", "West London"],
            job_centre_label="sutton"
        )
        area.save()
        ja = JobAdvert(
            title="Test",
            location_text="Diss, Norfolk",
            job_area=area
        )

        self.assertTrue(ja.calculate_travelling_time() > 90)

        ja = JobAdvert(
            title="Test",
            location_text="SM1 1PX",
            job_area=area
        )

        self.assertTrue(ja.calculate_travelling_time() < 90)

        ja = JobAdvert(
            title="Test",
            location_text="ASDASDASDASDASDASDASDADASDAD",
            job_area=area
        )

        self.assertEqual(ja.calculate_travelling_time(), -1)
