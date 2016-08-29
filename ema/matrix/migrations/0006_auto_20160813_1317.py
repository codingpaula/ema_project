# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrix', '0005_auto_20160725_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='color',
            field=models.CharField(default='black', max_length=15, choices=[('black', 'black'), ('grey', 'grey'), ('rosybrown', 'rosybrown'), ('saddlebrown', 'brown'), ('crimson', 'red'), ('orangered', 'orangered'), ('darkorange', 'orange'), ('gold', 'yellow'), ('yellowgreen', 'lightgreen'), ('olivedrab', 'olive'), ('forestgreen', 'green'), ('darkturquoise', 'turquoise'), ('dodgerblue', 'lightblue'), ('royalblue', 'royalblue'), ('mediumblue', 'blue'), ('hotpink', 'pink'), ('deeppink', 'deeppink'), ('mediumvioletred', 'violet'), ('purple', 'purple'), ('rebeccapurple', 'darkpurple'), ('mediumorchid', 'orchid')]),
        ),
    ]
