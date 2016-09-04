# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('matrix', '0007_auto_20160901_1147'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserOrga',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('urgent_axis', models.CharField(default=b'1', max_length=1, choices=[(b'0', b'1 month'), (b'1', b'2 months'), (b'2', b'4 months')])),
                ('tele_username', models.CharField(default=b'', max_length=30, blank=True)),
                ('default_topic', models.ForeignKey(default=None, to='matrix.Topic', null=True)),
                ('owner', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
