from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import filters

from .serializers import JobAdvertSerializer
from jobs.models import JobAdvert


class DummyDashboardView(APIView):
    def get(self, request, format=None):

        # This is just made up dummy data
        dummy_data = {
            'content': 'test',
            'status': 1,
        }

        return Response(dummy_data)


class JobAdvertViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = JobAdvert.objects.all().order_by("-created")
    serializer_class = JobAdvertSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('job_centre_label',)
