from rest_framework.views import APIView
from rest_framework.response import Response

from .adzuna import Adzuna


class DummyDashboardView(APIView):
    def get(self, request, format=None):

        # This is just made up dummy data
        dummy_data = {
            'content': 'test',
            'status': 1,
        }

        return Response(dummy_data)


class LatestJobsInArea(APIView):
    def get(self, request):

        #Hard code location for now
        location0 = "UK"
        location1 = "London"
        location2 = "South East London"

        az = Adzuna()

        results = az.jobs_at_loation(location0, location1, location2)

        all_results = []
        import json
        for result in results.json()['results']:
            # import ipdb; ipdb.set_trace()
            all_results.append({
                "job_title": result['title'],
                "company": {
                    "display_name": result['company']['display_name']
                },
                "created": result['created'],
                "job_category": result['category']['label'],
            })

        return Response(all_results)