# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orga', '0003_remove_userorga_tele_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='userorga',
            name='tele_username',
            field=models.TextField(max_length=30, blank=True),
        ),
    ]
