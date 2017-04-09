# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrix', '0008_auto_20160929_1538'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='duration',
            field=models.FloatField(default=1, blank=True),
        ),
    ]
