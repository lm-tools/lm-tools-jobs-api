from django.db.models import Count
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import JobAdvertSerializer
from jobs.models import JobAdvert, JobArea, UnknownJobCentreError, PostcodeNotFoundError
from .adzuna import Adzuna


class DummyDashboardView(APIView):
    def get(self, request, format=None):

        # This is just made up dummy data
        dummy_data = {
            'content': 'test',
            'status': 1,
        }

        return Response(dummy_data)

class JobAdvertsView(APIView):
    def get(self, request):
        serializer_class = JobAdvertSerializer
        base_qs = JobAdvert.objects.all()
        # This is a duplicate
        job_area = None
        if 'job_centre_label' in request.GET:
            try:
                job_area = JobArea.objects.import_area_and_jobs_for_job_centre(request.GET['job_centre_label'])
            except UnknownJobCentreError:
                return Response({"error": "Unknown job centre label"})
        if 'postcode' in request.GET:
            try:
                job_area = JobArea.objects.import_area_and_jobs_for_postcode(request.GET['postcode'])
            except PostcodeNotFoundError:
                return Response({"error": "Invalid postcode"})
        # End of duplicate
        if job_area:
            base_qs = base_qs.filter(job_area=job_area)
        limit = request.GET.get('limit', 5)
        ret = base_qs[:limit]
        return Response(ret)


class TopCategoriesView(APIView):
    def get(self, request):
        base_qs = JobAdvert.objects.all()
        # This is a duplicate
        job_area = None
        if 'job_centre_label' in request.GET:
            try:
                job_area = JobArea.objects.import_area_and_jobs_for_job_centre(request.GET['job_centre_label'])
            except UnknownJobCentreError:
                return Response({"error": "Unknown job centre label"})
        if 'postcode' in request.GET:
            try:
                job_area = JobArea.objects.import_area_and_jobs_for_postcode(request.GET['postcode'])
            except PostcodeNotFoundError:
                return Response({"error": "Invalid postcode"})
        # End of duplicate
        if job_area:
            base_qs = base_qs.filter(job_area=job_area)
        limit = request.GET.get('limit', 5)
        ret = base_qs.values("category").annotate(count=Count("category")).order_by("-count")[:limit]
        return Response(ret)


class TopCompaniesView(APIView):
     def get(self, request):
        # This is a duplicate
        job_area = None
        if 'job_centre_label' in request.GET:
            try:
                job_area = JobArea.objects.import_area_and_jobs_for_job_centre(request.GET['job_centre_label'])
            except UnknownJobCentreError:
                return Response({"error": "Unknown job centre label"})
        if 'postcode' in request.GET:
            try:
                job_area = JobArea.objects.import_area_and_jobs_for_postcode(request.GET['postcode'])
            except PostcodeNotFoundError:
                return Response({"error": "Invalid postcode"})
        # End of duplicate

        all_results = []
        az = Adzuna()
        if job_area:
            args = job_area.locations
            args.append(int(request.GET.get("count", 10)))
            results = az.top_companies(*args)
            all_results = []
            for result in results:
                all_results.append({
                    "company_name": result['canonical_name'],
                })

        return Response(all_results)
