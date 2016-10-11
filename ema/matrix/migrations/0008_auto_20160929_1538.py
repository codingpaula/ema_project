# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrix', '0007_auto_20160901_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_description',
            field=models.TextField(max_length=3000, blank=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='topic_description',
            field=models.TextField(max_length=2000, blank=True),
        ),
    ]
