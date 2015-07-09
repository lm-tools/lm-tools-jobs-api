# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JobAdvert',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('raw_data', models.TextField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('contract_time', models.CharField(blank=True, max_length=255, null=True)),
                ('compay_name', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('category', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
