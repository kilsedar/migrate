# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0004_auto_20160822_0939'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='country',
            field=models.ForeignKey(default=1, verbose_name='country', to='players.Country'),
        ),
    ]
