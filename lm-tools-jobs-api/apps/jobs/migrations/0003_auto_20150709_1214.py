# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_jobadvert_job_centre_label'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jobadvert',
            old_name='compay_name',
            new_name='company_name',
        ),
    ]
