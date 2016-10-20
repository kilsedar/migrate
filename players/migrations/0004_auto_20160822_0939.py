# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0003_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='country',
        ),
        migrations.AlterField(
            model_name='player',
            name='user',
            field=models.OneToOneField(verbose_name='player', to=settings.AUTH_USER_MODEL),
        ),
    ]
