# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrix', '0011_task_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='importance',
            field=models.IntegerField(default=1, choices=[(0, 'not important'), (1, 'less important'), (2, 'important'), (3, 'very important')]),
        ),
    ]
