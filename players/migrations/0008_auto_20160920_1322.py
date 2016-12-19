# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0007_auto_20160916_1520'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ['country'], 'verbose_name_plural': 'countries'},
        ),
    ]
