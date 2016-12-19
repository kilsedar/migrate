# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0006_auto_20160916_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='fixed',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
    ]
