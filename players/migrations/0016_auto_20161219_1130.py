# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0015_profile_avg_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='n_games',
            field=models.IntegerField(default=None, null=True, verbose_name='number of games', blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='n_games_quitted',
            field=models.IntegerField(default=None, null=True, verbose_name='number of games quitted', blank=True),
        ),
    ]
