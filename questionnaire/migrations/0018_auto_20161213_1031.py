# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0017_auto_20161213_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answeredquestion',
            name='eval',
            field=models.TextField(default='---', null=True, verbose_name='evaluation', blank=True),
        ),
    ]
