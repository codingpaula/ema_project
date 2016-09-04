# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orga', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userorga',
            name='tele_username',
            field=models.TextField(max_length=30, blank=True),
        ),
    ]
