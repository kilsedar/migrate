# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0010_auto_20161102_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='education',
            field=models.CharField(default=None, max_length=20, verbose_name='education level', choices=[(None, '---------'), ('ps', 'Primary school'), ('ss', 'Secondary school'), ('college', 'College degree'), ('bachelor', 'Bachelor degree'), ('master', 'Master degree'), ('phd', 'PhD degree'), ('other', 'Other')]),
        ),
    ]
