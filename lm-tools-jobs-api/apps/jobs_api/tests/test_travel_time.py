from django.test import TestCase

from jobs.models import JobAdvert


class TestViews(TestCase):

    def test_travel_time(self):
        ja = JobAdvert(
            title="Test",
            location_text="Diss, Norfolk",
        )

        self.assertEqual(bool(ja.calculate_travelling_time()), True)