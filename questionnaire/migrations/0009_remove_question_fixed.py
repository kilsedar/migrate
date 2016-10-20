# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0008_fixedanswers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='fixed',
        ),
    ]
