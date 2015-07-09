from rest_framework import serializers

from jobs.models import JobAdvert

class JobAdvertSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobAdvert



