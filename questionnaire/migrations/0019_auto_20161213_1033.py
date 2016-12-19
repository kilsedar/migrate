# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0018_auto_20161213_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answeredquestion',
            name='eval',
            field=models.TextField(default='None', verbose_name='evaluation'),
        ),
    ]
