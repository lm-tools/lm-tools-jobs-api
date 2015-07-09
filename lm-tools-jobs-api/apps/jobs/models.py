from django.db import models

from jobs_api.adzuna import Adzuna


class JobAdvertManager(models.Manager):
    def import_from_adzuna(self, job_centre, location_str, count):
        """
        Method to import jobs from the Adzuna API
        """
        args = location_str.split(',')
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

    objects = JobAdvertManager()

    def __str__(self):
        category = getattr(self, "category") or  "Unknown"
        return "{category} ({title})".format(
            category=category,
            title=self.title,
        )

    @classmethod
    def get_or_create_from_adzuna(cls, job_centre, job):
        obj = cls.objects.get_or_create(
                job_centre_label=job_centre,
                title=job['title'],
                created=job['created'],
                defaults={
                    "category": job['category']['label']
                }
            )

    
