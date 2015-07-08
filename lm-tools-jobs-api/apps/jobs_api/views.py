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

        location0 = request.GET.get("location0", "UK")
        location1 = request.GET.get("location1", "London")
        location2 = request.GET.get("location2", "South East London")
        count =  int(request.GET.get("count", 10))

        az = Adzuna()

        results = az.jobs_at_location(location0, location1, location2, count)

        all_results = []
        for result in results:
            all_results.append({
                "job_title": result['title'],
                "contract_time": result.get('contract_time', "full_time"),
                "company": {
                    "display_name": result['company']['display_name']
                },
                "created": result['created'],
                "job_category": result['category']['label'],
            })

        return Response(all_results)