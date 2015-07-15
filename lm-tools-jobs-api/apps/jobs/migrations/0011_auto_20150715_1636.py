# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0010_auto_20150715_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobarea',
            name='job_centre_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
