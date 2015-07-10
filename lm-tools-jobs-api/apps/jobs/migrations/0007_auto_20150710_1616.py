# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0006_auto_20150709_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobadvert',
            name='travelling_time',
            field=models.CharField(max_length=100, blank=True, null=True),
        ),
    ]
