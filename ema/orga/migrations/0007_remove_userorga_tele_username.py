# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orga', '0006_auto_20160929_1542'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userorga',
            name='tele_username',
        ),
    ]
