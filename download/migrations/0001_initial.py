# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Download',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=None, max_length=20, verbose_name='name')),
                ('surname', models.CharField(default=None, max_length=20, verbose_name='surname')),
                ('email', models.EmailField(default=None, max_length=30, verbose_name='email')),
                ('affiliation', models.CharField(default=None, max_length=500, verbose_name='affiliation')),
                ('project_name', models.CharField(default=None, max_length=500, verbose_name='name of the project, initiative, study or application')),
                ('project_description', models.CharField(default=None, max_length=1000, verbose_name='brief description of the project, initiative, study or application')),
            ],
        ),
    ]
