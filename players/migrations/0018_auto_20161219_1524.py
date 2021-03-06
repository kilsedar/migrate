# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0017_auto_20161219_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avg_score',
            field=models.FloatField(null=True, verbose_name='avg score', blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='total_score',
            field=models.FloatField(null=True, verbose_name='total score', blank=True),
        ),
    ]
