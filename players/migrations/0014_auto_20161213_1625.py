# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0013_auto_20161212_1743'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='avg_score',
        ),
        migrations.AddField(
            model_name='profile',
            name='total_score',
            field=models.FloatField(default=0, null=True, verbose_name='total score', blank=True),
        ),
    ]
