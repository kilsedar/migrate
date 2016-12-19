# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0011_game'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='cnt_list',
            field=models.CharField(max_length=599, blank=True),
        ),
    ]
