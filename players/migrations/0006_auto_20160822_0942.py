# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0005_player_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='country',
            field=models.ForeignKey(default=1, verbose_name='country', to='players.Country'),
        ),
    ]
