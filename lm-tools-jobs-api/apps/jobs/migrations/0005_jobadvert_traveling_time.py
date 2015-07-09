# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_jobadvert_location_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobadvert',
            name='traveling_time',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
