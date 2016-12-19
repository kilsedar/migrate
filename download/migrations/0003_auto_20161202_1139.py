# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('download', '0002_auto_20161109_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='download',
            name='project_description',
            field=models.CharField(default=None, max_length=1000, verbose_name='brief description of this project, initiative, study or application'),
        ),
        migrations.AlterField(
            model_name='download',
            name='project_name',
            field=models.CharField(default=None, max_length=500, verbose_name='name of the project, initiative, study or application using MIGRATE data'),
        ),
    ]
