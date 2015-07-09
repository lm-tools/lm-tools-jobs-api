# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_jobadvert_traveling_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jobadvert',
            old_name='traveling_time',
            new_name='travelling_time',
        ),
    ]
