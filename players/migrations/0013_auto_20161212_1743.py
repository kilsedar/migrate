# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0012_auto_20161201_0959'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='n_games',
            field=models.IntegerField(null=True, verbose_name='number of games', blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='n_games_quitted',
            field=models.IntegerField(null=True, verbose_name='number of games quitted', blank=True),
        ),
    ]
