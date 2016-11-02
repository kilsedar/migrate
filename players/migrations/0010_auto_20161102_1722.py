# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0009_auto_20161004_0931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='age',
            field=models.CharField(default=None, help_text='I hereby certify that I am 18 years of age or older.', max_length=10, verbose_name='age range (years)', choices=[(None, '---------'), ('18_24', '18 - 24'), ('25_34', '25 - 34'), ('35_44', '35 - 44'), ('45_54', '45 - 54'), ('55_64', '55 - 64'), ('more_65', '65 or more')]),
        ),
        migrations.AlterField(
            model_name='player',
            name='country',
            field=models.ForeignKey(default=None, verbose_name='country of origin', to='players.Country'),
        ),
        migrations.AlterField(
            model_name='player',
            name='education',
            field=models.CharField(default='ps', max_length=20, verbose_name='education level', choices=[(None, '---------'), ('ps', 'Primary school'), ('ss', 'Secondary school'), ('college', 'College degree'), ('bachelor', 'Bachelor degree'), ('master', 'Master degree'), ('phd', 'PhD degree'), ('other', 'Other')]),
        ),
        migrations.AlterField(
            model_name='player',
            name='gender',
            field=models.CharField(default=None, max_length=10, verbose_name='gender', choices=[(None, '---------'), ('f', 'Female'), ('m', 'Male'), ('ns', 'Not specified')]),
        ),
        migrations.AlterField(
            model_name='player',
            name='profile',
            field=models.OneToOneField(verbose_name='profile', to='players.Profile'),
        ),
    ]
