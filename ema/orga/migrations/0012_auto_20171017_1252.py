# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orga', '0011_auto_20170615_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userorga',
            name='urgent_axis',
            field=models.IntegerField(default=1, choices=[(3, b'1 week'), (4, b'2 weeks'), (0, b'1 month'), (1, b'2 months'), (2, b'4 months')]),
        ),
    ]
