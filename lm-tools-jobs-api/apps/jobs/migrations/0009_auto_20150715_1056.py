# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0008_jobarea'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobadvert',
            name='job_centre_label',
        ),
        migrations.AddField(
            model_name='jobadvert',
            name='job_area',
            field=models.ForeignKey(default='', blank=True, to='jobs.JobArea'),
            preserve_default=False,
        ),
    ]
