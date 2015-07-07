from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase


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
