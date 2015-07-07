"""
Helper class for working with the adzuna API
"""

import requests

from django.conf import settings

class Adzuna(object):
    def __init__(self):
        self.APP_ID = getattr(settings, 'ADZUNA_APP_ID')
        self.APP_KEY = getattr(settings, 'ADZUNA_APP_KEY')
        self.BASE_URL = "http://api.adzuna.com:80/v1/api/"

        assert all((self.APP_ID, self.APP_KEY))


    def base_request(self, endpoint, params, page=1):
        URL = "{0}{1}/{2}".format(self.BASE_URL, endpoint, page)

        params.update({
            "app_id": self.APP_ID,
            "app_key": self.APP_KEY,
        })

        return requests.get(URL, params=params)


    def unwrap_pagination(self, endpoint, params, count):
        num_results = 0
        all_results = []
        page = 1

        while num_results <= count:
            results = self.base_request(endpoint, params, page)
            all_results += results.json()['results']
            page += 1
            num_results = len(all_results)
        return all_results[:count]

    def jobs_at_loation(self, location0, location1, location2, count=10):
        endpoint = "jobs/gb/search/"

        params = {
            "location0": location0,
            "location1": location1,
            "location2": location2,
        }

        return self.unwrap_pagination(endpoint, params, count)