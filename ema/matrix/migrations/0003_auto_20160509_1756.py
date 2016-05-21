# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrix', '0002_auto_20160426_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='topic',
            name='color',
            field=models.TextField(default='red'),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='topic_description',
            field=models.TextField(blank=True),
        ),
    ]
