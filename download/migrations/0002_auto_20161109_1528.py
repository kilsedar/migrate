# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('download', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='download',
            name='affiliation',
            field=models.CharField(default=None, max_length=500, verbose_name='affiliation', blank=True),
        ),
        migrations.AlterField(
            model_name='download',
            name='name',
            field=models.CharField(default=None, max_length=20, verbose_name='name', blank=True),
        ),
        migrations.AlterField(
            model_name='download',
            name='surname',
            field=models.CharField(default=None, max_length=20, verbose_name='surname', blank=True),
        ),
    ]
