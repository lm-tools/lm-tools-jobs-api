# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_auto_20150709_1214'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobadvert',
            name='location_text',
            field=models.CharField(max_length=500, blank=True),
        ),
    ]
