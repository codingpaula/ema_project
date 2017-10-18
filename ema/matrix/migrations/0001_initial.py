# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('task_name', models.CharField(max_length=50)),
                ('task_description', models.TextField(max_length=3000, blank=True)),
                ('importance', models.IntegerField(default=1, choices=[(0, 'not important'), (1, 'less important'), (2, 'important'), (3, 'very important')])),
                ('due_date', models.DateTimeField()),
                ('done', models.BooleanField(default=False)),
                ('duration', models.FloatField(default=1, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('topic_name', models.CharField(max_length=30)),
                ('topic_description', models.TextField(max_length=2000, blank=True)),
                ('color', models.CharField(default='black', max_length=15, choices=[('black', 'black'), ('grey', 'grey'), ('rosybrown', 'rosybrown'), ('saddlebrown', 'brown'), ('crimson', 'red'), ('orangered', 'orangered'), ('darkorange', 'orange'), ('gold', 'yellow'), ('yellowgreen', 'lightgreen'), ('olivedrab', 'olive'), ('forestgreen', 'green'), ('darkturquoise', 'turquoise'), ('dodgerblue', 'lightblue'), ('royalblue', 'royalblue'), ('mediumblue', 'blue'), ('hotpink', 'pink'), ('deeppink', 'deeppink'), ('mediumvioletred', 'violet'), ('purple', 'purple'), ('rebeccapurple', 'darkpurple'), ('mediumorchid', 'orchid')])),
                ('topic_owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='task',
            name='topic',
            field=models.ForeignKey(to='matrix.Topic'),
        ),
    ]
