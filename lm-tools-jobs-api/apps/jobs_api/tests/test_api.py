import os
from functools import wraps

from django.core.urlresolvers import reverse
from django.conf import settings

from rest_framework.test import APITestCase

from jobs.models import JobAdvert
from jobs.models import JobArea


def adzuna_api_cassette_request(func):
    @wraps(func)
    def innner(*args, **kwargs):
        filter_args = [
            'app_key',
            'app_id',
        ]

        # TODO This need to be more clever, as right now it will always
        #      save cassettes relative to this file.
        path = os.path.join(os.path.dirname(__file__), func.__name__)
        with settings.VCR.use_cassette(path, filter_query_parameters=filter_args):
            func(*args, **kwargs)
    return innner



class TestViews(APITestCase):

    def test_dummy_view(self):
        url = reverse('dummy_api_view')
        self.assertEqual(
            self.client.get(url).data,
            {
                    'content': 'test',
                    'status': 1,
                },
        )

    def test_latest_jobs(self):
        area = JobArea(locations=["Universe", "Narnia", "Aslan County"])
        area.save()
        ja = JobAdvert(title="test", job_area=area)
        ja.save()
        res = self.client.get(reverse('job_adverts_view'))
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], "test")

    def test_latest_jobs_unknown_job_centre_label(self):
        res = self.client.get(reverse('job_adverts_view'), {'job_centre_label': 'not-a-valid-job-centre'})
        self.assertEqual(res.data['error'], 'Unknown job centre label')

    @adzuna_api_cassette_request
    def test_latest_jobs_by_job_centre_label(self):
        area = JobArea(locations=["UK", "London", "South East London"], job_centre_label="sutton")
        area.save()
        ja = JobAdvert(title="test", job_area=area)
        ja.save()
        res = self.client.get(reverse('job_adverts_view'), {'job_centre_label': 'sutton'})
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], "test")

    @adzuna_api_cassette_request
    def test_latest_jobs_by_new_job_centre_label(self):
        res = self.client.get(reverse('job_adverts_view'), {'job_centre_label': 'sutton', 'limit': 3})
        areas = JobArea.objects.all()
        self.assertEqual(areas.count(), 1)
        self.assertEqual(areas[0].locations, ["UK", "London", "South East London"])
        self.assertEqual(areas[0].job_centre_label, "sutton")
        self.assertEqual(len(res.data), 3)

    @adzuna_api_cassette_request
    def test_latest_jobs_by_postcode_new_location(self):
        res = self.client.get(reverse('job_adverts_view'), {'postcode': 'EH1 2NG', 'limit': 3})
        areas = JobArea.objects.all()
        self.assertEqual(areas.count(), 1)
        self.assertEqual(areas[0].locations, ["UK", "Scotland", "Edinburgh"])
        self.assertEqual(areas[0].job_centre_label, None)
        self.assertEqual(len(res.data), 3)

    @adzuna_api_cassette_request
    def test_latest_jobs_by_postcode_new_location_matching_a_job_centre(self):
        res = self.client.get(reverse('job_adverts_view'), {'postcode': 'CR9 2TN', 'limit': 3})
        areas = JobArea.objects.all()
        self.assertEqual(areas.count(), 1)
        self.assertEqual(areas[0].locations, ["UK", "London", "Croydon"])
        self.assertEqual(areas[0].job_centre_label, "croydon")
        self.assertEqual(len(res.data), 3)

    @adzuna_api_cassette_request
    def test_latest_jobs_by_postcode_existing_location(self):
        res = self.client.get(reverse('job_adverts_view'), {'postcode': 'CR9 2TN', 'limit': 3})
        res2 = self.client.get(reverse('job_adverts_view'), {'postcode': 'CR0 1LP', 'limit': 3})
        areas = JobArea.objects.all()
        self.assertEqual(areas.count(), 1)
        self.assertEqual(len(res2.data), 3)

    def test_top_companies(self):
        res = self.client.get(reverse('top_companies_view'))
        self.assertEqual(len(res.data), 0)

    def test_top_companies_invalid_postcode(self):
        res = self.client.get(reverse('top_companies_view'), {'postcode': 'invalid'})
        self.assertEqual(res.data['error'], 'Invalid postcode')

    @adzuna_api_cassette_request
    def test_top_companies_valid_postcode(self):
        res = self.client.get(reverse('top_companies_view'), {'postcode': 'SW1H0ET'})
        self.assertEqual(len(res.data), 5)
        self.assertTrue('company_name' in res.data[0])

    def test_top_categories(self):
        area = JobArea(locations=["Universe", "Narnia", "Aslan County"])
        area.save()
        ja = JobAdvert(title="test", category="Foo", job_area=area)
        ja.save()
        res = self.client.get(reverse('top_categories_view'))
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['category'], "Foo")
        self.assertEqual(res.data[0]['count'], 1)

    def test_top_categories_unknown_job_centre_label(self):
        res = self.client.get(reverse('top_categories_view'), {'job_centre_label': 'not-a-valid-job-centre'})
        self.assertEqual(res.data['error'], 'Unknown job centre label')

    @adzuna_api_cassette_request
    def test_top_categories_by_job_centre_label(self):
        area = JobArea(locations=["UK", "London", "South East London"], job_centre_label="sutton")
        area.save()
        ja = JobAdvert(title="test", category="Foo", job_area=area)
        ja.save()
        res = self.client.get(reverse('top_categories_view'), {'job_centre_label': 'sutton'})
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['category'], "Foo")
        self.assertEqual(res.data[0]['count'], 1)

    @adzuna_api_cassette_request
    def test_top_categories_by_postcode_new_location(self):
        res = self.client.get(reverse('top_categories_view'), {'postcode': 'EH1 2NG', 'limit': 3})
        areas = JobArea.objects.all()
        self.assertEqual(areas.count(), 1)
        self.assertEqual(areas[0].locations, ["UK", "Scotland", "Edinburgh"])
        self.assertEqual(areas[0].job_centre_label, None)
        self.assertEqual(len(res.data), 3)

    @adzuna_api_cassette_request
    def test_top_categories_by_postcode_new_location_matching_a_job_centre(self):
        res = self.client.get(reverse('top_categories_view'), {'postcode': 'CR9 2TN', 'limit': 3})
        areas = JobArea.objects.all()
        self.assertEqual(areas.count(), 1)
        self.assertEqual(areas[0].locations, ["UK", "London", "Croydon"])
        self.assertEqual(areas[0].job_centre_label, "croydon")
        self.assertEqual(len(res.data), 3)

    @adzuna_api_cassette_request
    def test_top_categories_by_postcode_existing_location(self):
        res = self.client.get(reverse('top_categories_view'), {'postcode': 'CR9 2TN'})
        res2 = self.client.get(reverse('top_categories_view'), {'postcode': 'CR0 1LP', 'limit': 3})
        areas = JobArea.objects.all()
        self.assertEqual(areas.count(), 1)
        self.assertEqual(len(res2.data), 3)
