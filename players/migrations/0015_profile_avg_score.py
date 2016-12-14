# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0014_auto_20161213_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avg_score',
            field=models.FloatField(default=0, null=True, verbose_name='avg score', blank=True),
        ),
    ]
