# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orga', '0004_userorga_tele_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userorga',
            name='default_topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='matrix.Topic', null=True),
        ),
        migrations.AlterField(
            model_name='userorga',
            name='tele_username',
            field=models.TextField(max_length=30, unique=True, null=True, blank=True),
        ),
    ]
