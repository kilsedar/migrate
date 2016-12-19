# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0007_question_fixed'),
    ]

    operations = [
        migrations.CreateModel(
            name='FixedAnswers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('option2', models.TextField(blank=True)),
                ('option3', models.TextField(blank=True)),
                ('option4', models.TextField(blank=True)),
                ('question', models.OneToOneField(to='questionnaire.Question')),
            ],
        ),
    ]
