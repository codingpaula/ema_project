# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orga', '0010_remove_userorga_default_topic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userorga',
            name='urgent_axis',
            field=models.CharField(default=1, max_length=1, choices=[(0, b'1 month'), (1, b'2 months'), (2, b'4 months')]),
        ),
    ]
