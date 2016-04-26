# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('matrix', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='date_complete',
            new_name='due_date',
        ),
        migrations.RemoveField(
            model_name='task',
            name='date_created',
        ),
        migrations.AddField(
            model_name='task',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 26, 20, 15, 2, 40131, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 26, 20, 15, 11, 576117, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='topic',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 26, 20, 15, 32, 71100, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='topic',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 26, 20, 15, 37, 999175, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
