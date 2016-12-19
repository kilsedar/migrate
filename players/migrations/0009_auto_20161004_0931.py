# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0008_auto_20160920_1322'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('avg_score', models.IntegerField(null=True, verbose_name='average score', blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='player',
            name='country',
            field=models.ForeignKey(default=1, verbose_name='country of origin', to='players.Country'),
        ),
        migrations.AddField(
            model_name='player',
            name='profile',
            field=models.OneToOneField(null=True, blank=True, to='players.Profile', verbose_name='profile'),
        ),
    ]
