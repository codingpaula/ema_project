# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('matrix', '0003_auto_20160509_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='topic_owner',
            field=models.ForeignKey(default=2, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='topic',
            name='color',
            field=models.CharField(default='red', max_length=15),
        ),
    ]
