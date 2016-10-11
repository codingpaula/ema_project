# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orga', '0007_remove_userorga_tele_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='userorga',
            name='tele_username',
            field=models.TextField(default=None, max_length=30, null=True, blank=True),
        ),
    ]
