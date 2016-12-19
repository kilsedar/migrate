# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0016_auto_20161219_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avg_score',
            field=models.FloatField(default=None, null=True, verbose_name='avg score', blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='n_games',
            field=models.IntegerField(default=0, null=True, verbose_name='number of games', blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='n_games_quitted',
            field=models.IntegerField(default=0, null=True, verbose_name='number of games quitted', blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='total_score',
            field=models.FloatField(default=None, null=True, verbose_name='total score', blank=True),
        ),
    ]
