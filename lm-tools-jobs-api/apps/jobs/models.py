from django.db import models

import requests

from jobs_api.adzuna import Adzuna


class JobAdvertManager(models.Manager):
    def import_from_adzuna(self, job_centre, count):
        """
        Method to import jobs from the Adzuna API
        """
        args = getattr(settings, 'LOCATION_LABELS')[job_centre]['locations']
        args.append(count)

        az = Adzuna()
        all_jobs = az.jobs_at_location(*args)
        for job in all_jobs:
            JobAdvert.get_or_create_from_adzuna(job_centre, job)


class JobAdvert(models.Model):
    raw_data = models.TextField(blank=True, null=True)
    title = models.CharField(blank=True, max_length=255, null=True)
    contract_time = models.CharField(blank=True, max_length=255, null=True)
    company_name = models.CharField(blank=True, max_length=255, null=True)
    created = models.DateTimeField(blank=True, null=True)
    category = models.CharField(blank=True, max_length=255, null=True)
    job_centre_label = models.CharField(blank=True, max_length=255)
    location_text = models.CharField(blank=True, max_length=500)
    travelling_time = models.CharField(blank=True, max_length=100)

    objects = JobAdvertManager()

    def __str__(self):
        category = getattr(self, "category") or  "Unknown"
        return "{category} ({title})".format(
            category=category,
            title=self.title,
        )

    @classmethod
    def get_or_create_from_adzuna(cls, job_centre, job):
        def _mk_location_text(job):
            area = job['location']['area']
            area.reverse()
            return ", ".join(area)

        obj, created = cls.objects.get_or_create(
                job_centre_label=job_centre,
                title=job['title'],
                created=job['created'],
                defaults={
                    "category": job['category']['label'],
                }
            )
        obj.location_text = _mk_location_text(job)
        obj.calculate_travelling_time()
        obj.save()


    def calculate_travelling_time(self, force=False):
        if self.travelling_time != "" and not force:
            return self.travelling_time

        params = {
            "origin":  "jobcentre plus, {0}, London, UK".format(self.job_centre_label),
            "destination":  self.location_text,
            "mode":  "transit",
        }
        try:
            results = requests.get("https://maps.googleapis.com/maps/api/directions/json",
                params=params).json()

            travelling_time = results['routes'][0]['legs'][0]['duration']['text']
            travelling_time = travelling_time.replace('mins', 'minutes')
            self.travelling_time = travelling_time
            self.save()
        except:
            return "Unknown"
        return self.travelling_time
