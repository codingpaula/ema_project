# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orga', '0002_auto_20160901_1213'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userorga',
            name='tele_username',
        ),
    ]
