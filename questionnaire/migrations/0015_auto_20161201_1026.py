# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0014_auto_20161004_0925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='score',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
