# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0007_auto_20150710_1616'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobArea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('locations', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True), size=3)),
            ],
        ),
    ]
