# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task_name', models.CharField(max_length=200)),
                ('task_description', models.TextField()),
                ('importance', models.CharField(default='1', max_length=1, choices=[('0', 'not important'), ('1', 'less important'), ('2', 'important'), ('3', 'very important')])),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_complete', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('topic_name', models.CharField(max_length=30)),
                ('topic_description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='topic',
            field=models.ForeignKey(to='matrix.Topic'),
        ),
    ]
