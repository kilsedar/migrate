# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Download(models.Model):

    name = models.CharField(max_length=20, blank=True, default=None, verbose_name=u'name')
    surname = models.CharField(max_length=20, blank=True, default=None, verbose_name=u'surname')
    email = models.EmailField(max_length=30, blank=False, default=None, verbose_name=u'email')
    affiliation = models.CharField(max_length=500, blank=True, default=None, verbose_name=u'affiliation')
    project_name = models.CharField(max_length=500, blank=False, default=None, verbose_name=u'name of the project, initiative, study or application')
    project_description = models.CharField(max_length=1000, blank=False, default=None, verbose_name=u'brief description of the project, initiative, study or application')

    def __unicode__(self):
        return self.name + " " + self.surname
