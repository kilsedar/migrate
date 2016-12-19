# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0013_answeredquestion_game'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='game',
            options={'ordering': ['-date']},
        ),
        migrations.AlterField(
            model_name='answeredquestion',
            name='option1',
            field=models.TextField(null=True, verbose_name='option 1', blank=True),
        ),
        migrations.AlterField(
            model_name='answeredquestion',
            name='option2',
            field=models.TextField(null=True, verbose_name='option 2', blank=True),
        ),
        migrations.AlterField(
            model_name='answeredquestion',
            name='option3',
            field=models.TextField(null=True, verbose_name='option 3', blank=True),
        ),
        migrations.AlterField(
            model_name='answeredquestion',
            name='option4',
            field=models.TextField(null=True, verbose_name='option 4', blank=True),
        ),
        migrations.AlterField(
            model_name='answeredquestion',
            name='user_answer',
            field=models.TextField(verbose_name='user answer', blank=True),
        ),
        migrations.AlterField(
            model_name='fixedanswers',
            name='option2',
            field=models.TextField(verbose_name='option 2', blank=True),
        ),
        migrations.AlterField(
            model_name='fixedanswers',
            name='option3',
            field=models.TextField(verbose_name='option 3', blank=True),
        ),
        migrations.AlterField(
            model_name='fixedanswers',
            name='option4',
            field=models.TextField(verbose_name='option 4', blank=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='score',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
