from rest_framework.views import APIView
from rest_framework.response import Response


class DummyDashboardView(APIView):
    def get(self, request, format=None):

        # This is just made up dummy data
        dummy_data = {
            'content': 'test',
            'status': 1,
        }

        return Response(dummy_data)
