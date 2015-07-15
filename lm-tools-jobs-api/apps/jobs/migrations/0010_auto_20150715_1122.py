# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0009_auto_20150715_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobarea',
            name='job_centre_label',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='jobadvert',
            name='job_area',
            field=models.ForeignKey(to='jobs.JobArea'),
        ),
    ]
