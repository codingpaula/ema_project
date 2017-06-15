# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrix', '0010_remove_task_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='duration',
            field=models.FloatField(default=1, blank=True),
        ),
    ]
