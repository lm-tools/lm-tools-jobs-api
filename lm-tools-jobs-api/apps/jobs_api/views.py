from django.db.models import Count
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
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
        base_qs = JobAdvert.objects.all().order_by('-created')
        try:
            job_area = JobArea.objects.import_area_and_jobs(request.GET.get('job_centre_label'), request.GET.get('postcode'))
        except UnknownJobCentreError:
            return Response({"error": "Unknown job centre label"})
        except PostcodeNotFoundError:
            return Response({"error": "Invalid postcode"})
        if job_area:
            base_qs = base_qs.filter(job_area=job_area)
        limit = int(request.GET.get('limit', 5))
        ret = base_qs[:limit]

        serialized_jobs = [{
            "title": job.title,
            "contract_time": job.contract_time,
            "company_name": job.company_name,
            "created": job.created,
            "category": job.category,
            "travelling_time": job.travelling_time
        } for job in ret]
        return Response(serialized_jobs)


class TopCategoriesView(APIView):
    def get(self, request):
        base_qs = JobAdvert.objects.all()
        try:
            job_area = JobArea.objects.import_area_and_jobs(request.GET.get('job_centre_label'), request.GET.get('postcode'))
        except UnknownJobCentreError:
            return Response({"error": "Unknown job centre label"})
        except PostcodeNotFoundError:
            return Response({"error": "Invalid postcode"})
        if job_area:
            base_qs = base_qs.filter(job_area=job_area)
        limit = int(request.GET.get('limit', 5))
        ret = base_qs.values("category").annotate(count=Count("category")).order_by("-count")[:limit]
        return Response(ret)


class TopCompaniesView(APIView):
     def get(self, request):
        try:
            job_area = JobArea.objects.import_area_and_jobs(request.GET.get('job_centre_label'), request.GET.get('postcode'))
        except UnknownJobCentreError:
            return Response({"error": "Unknown job centre label"})
        except PostcodeNotFoundError:
            return Response({"error": "Invalid postcode"})
        all_results = []
        az = Adzuna()
        if job_area:
            args = job_area.locations[:]
            args.append(int(request.GET.get("count", 10)))
            results = az.top_companies(*args)
            all_results = []
            for result in results:
                all_results.append({
                    "company_name": result['canonical_name'],
                })

        return Response(all_results)
