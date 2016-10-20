# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0009_remove_question_fixed'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnsweredQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_answer', models.TextField(blank=True)),
                ('option1', models.TextField(null=True, blank=True)),
                ('option2', models.TextField(null=True, blank=True)),
                ('option3', models.TextField(null=True, blank=True)),
                ('option4', models.TextField(null=True, blank=True)),
                ('question', models.ForeignKey(to='questionnaire.Question')),
            ],
        ),
    ]
