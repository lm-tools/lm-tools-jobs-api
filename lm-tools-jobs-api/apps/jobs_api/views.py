from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination

from .serializers import JobAdvertSerializer
from jobs.models import JobAdvert
from .adzuna import Adzuna


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
    pagination_class = LimitOffsetPagination


class TopCategoriesView(APIView):
    def get(self, request):
        base_qs = JobAdvert.objects.all()
        if 'job_centre_label' in request.GET:
            base_qs = base_qs.filter(job_centre_label=request.GET['job_centre_label'])
        ret = base_qs.values("category").annotate(count=Count("category")).order_by("-count")
        return Response(ret)


class TopCompaniesView(APIView):
     def get(self, request):
        job_centre_label = request.GET.get("job_centre_label", "sutton")
        count =  int(request.GET.get("count", 10))

        az = Adzuna()
        results = az.top_companies(job_centre_label, count)

        all_results = []
        for result in results:
            all_results.append({
                "company_name": result['canonical_name'],
            })

        return Response(all_results)
