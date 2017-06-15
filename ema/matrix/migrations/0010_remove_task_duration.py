# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrix', '0009_task_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='duration',
        ),
    ]
