# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0019_auto_20161213_1033'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='ip_address',
            field=models.TextField(null=True, verbose_name='ip address', blank=True),
        ),
    ]
