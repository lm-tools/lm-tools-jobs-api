from django.core.management.base import BaseCommand

from jobs.models import JobAdvert, JobArea


class Command(BaseCommand):
    help = 'Import job adverts from Adzuna at all areas currently stored'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int)

    def handle(self, *args, **options):
        for area in JobArea.objects.all():
            JobAdvert.objects.import_from_adzuna(
                area,
                options['count']
            )
