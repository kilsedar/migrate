# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0011_auto_20161109_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avg_score',
            field=models.FloatField(default=0, null=True, verbose_name='average score', blank=True),
        ),
    ]
