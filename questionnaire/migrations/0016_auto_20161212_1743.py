# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0015_auto_20161201_1026'),
    ]

    operations = [
        migrations.AddField(
            model_name='answeredquestion',
            name='eval',
            field=models.TextField(null=True, verbose_name='evaluation', blank=True),
        ),
        migrations.AddField(
            model_name='answeredquestion',
            name='trem',
            field=models.IntegerField(null=True, verbose_name='remaining time', blank=True),
        ),
    ]
