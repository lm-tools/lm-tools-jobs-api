from django.core.management.base import BaseCommand

from jobs.models import JobAdvert

class Command(BaseCommand):
    help = 'Import job adverts from Adzuna at a given location'

    def add_arguments(self, parser):
        parser.add_argument('job_centre', type=str)
        parser.add_argument('location', type=str)
        parser.add_argument('count', type=int)

    def handle(self, *args, **options):
        JobAdvert.objects.import_from_adzuna(
            options['job_centre'],
            options['location'],
            options['count']
        )
