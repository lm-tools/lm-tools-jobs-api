from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase

from jobs.models import JobAdvert


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
        ja = JobAdvert(title="test")
        ja.save()
        res = self.client.get(reverse('jobadvert-list'))
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], "test")