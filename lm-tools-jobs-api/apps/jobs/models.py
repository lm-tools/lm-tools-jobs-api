from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField


import requests

from jobs_api.adzuna import Adzuna


class UnknownJobCentreError(Exception):
    pass


class PostcodeNotFoundError(Exception):
    pass


class JobAreaManager(models.Manager):

    def import_area_and_jobs(self, job_centre_label, postcode):
        if job_centre_label:
            return JobArea.objects.\
                import_area_and_jobs_for_job_centre(job_centre_label)
        elif postcode:
            return JobArea.objects.import_area_and_jobs_for_postcode(postcode)
        else:
            return None

    def import_area_and_jobs_for_postcode(self, postcode):
        try:
            job_area, new_area = JobArea.get_or_create_from_postcode(postcode)
            if new_area:
                JobAdvert.objects.import_from_adzuna(job_area, 100)
            return job_area
        except PostcodeNotFoundError:
            raise PostcodeNotFoundError()

    def import_area_and_jobs_for_job_centre(self, job_centre_label):
        job_area, new_area = JobArea.\
            get_or_create_from_job_centre_label(job_centre_label)
        if new_area:
            JobAdvert.objects.import_from_adzuna(job_area, 100)
        return job_area


class JobArea(models.Model):
    locations = ArrayField(models.TextField(blank=True), size=3)
    job_centre_label = models.CharField(blank=True, max_length=255, null=True)

    objects = JobAreaManager()

    @classmethod
    def get_or_create_from_postcode(cls, postcode):
        az = Adzuna()
        try:
            locations = az.locations_for_postcode(postcode)
        except AssertionError:
            raise PostcodeNotFoundError()
        job_centre_label = None
        for location_label, location_list in settings.LOCATION_LABELS.items():
            if list(location_list['locations']) == locations:
                job_centre_label = location_label
                break
        obj, created = cls.objects.get_or_create(
            locations=locations,
            job_centre_label=job_centre_label
        )
        obj.save()
        return obj, created

    @classmethod
    def get_or_create_from_job_centre_label(cls, job_centre_label):
        try:
            locations = list(
                settings.LOCATION_LABELS[job_centre_label]['locations'])
        except KeyError:
            raise UnknownJobCentreError()
        obj, created = cls.objects.get_or_create(
            locations=locations,
            job_centre_label=job_centre_label
        )
        obj.save()
        return obj, created


class JobAdvertManager(models.Manager):
    def import_from_adzuna(self, job_area, count):
        """
        Method to import jobs from the Adzuna API
        """
        locations = job_area.locations
        args = list(locations) + [count]

        az = Adzuna()
        all_jobs = az.jobs_at_location(*args)
        for job in all_jobs:
            JobAdvert.get_or_create_from_adzuna(job_area, job)


class JobAdvert(models.Model):
    raw_data = models.TextField(blank=True, null=True)
    title = models.CharField(blank=True, max_length=255, null=True)
    contract_time = models.CharField(blank=True, max_length=255, null=True)
    company_name = models.CharField(blank=True, max_length=255, null=True)
    created = models.DateTimeField(blank=True, null=True)
    category = models.CharField(blank=True, max_length=255, null=True)
    job_area = models.ForeignKey(JobArea)
    location_text = models.CharField(blank=True, max_length=500)
    travelling_time = models.CharField(blank=True, max_length=100, null=True)

    objects = JobAdvertManager()

    def __str__(self):
        category = getattr(self, "category") or "Unknown"
        return "{category} ({title})".format(
            category=category,
            title=self.title,
        )

    @classmethod
    def get_or_create_from_adzuna(cls, job_area, job):
        def _mk_location_text(job):
            area = job['location']['area']
            area.reverse()
            return ", ".join(area)

        obj, created = cls.objects.get_or_create(
            job_area=job_area,
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
        if self.travelling_time and not force:
            return self.travelling_time
        if self.job_area.job_centre_label:
            params = {
                "origin": settings.LOCATION_LABELS[
                    self.job_area.job_centre_label]['postcode'],
                "destination": self.location_text,
                "mode": "transit",
            }
            try:
                url = "https://maps.googleapis.com/maps/api/directions/json"
                results = requests.get(url, params=params).json()
                travel_time_in_minutes = \
                    results['routes'][0]['legs'][0]['duration']['value'] / 60
                self.travelling_time = travel_time_in_minutes
            except:
                self.travelling_time = -1
        else:
            self.travelling_time = -1
        self.save()
        return self.travelling_time
