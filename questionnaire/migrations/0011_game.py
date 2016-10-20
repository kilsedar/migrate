# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0008_auto_20160920_1322'),
        ('questionnaire', '0010_answeredquestion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('player', models.ForeignKey(to='players.Player')),
            ],
        ),
    ]
