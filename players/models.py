# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
import json
import random
from django.db import models
from django.db.models import Q
from django.core.cache import cache
from django.contrib.auth.models import User

# Create your models here.
class Country(models.Model):
    class Meta:
        verbose_name_plural = 'countries'
        ordering = ["country"]

    REGIONS = (
     ("ITA", "Italy"),
     ("AFR", "Africa"),
     ("EUR", "Europe"),
     ("GRC", "Greece"),
     ("ESP", "Spain"),
     ("BLK", "Bulgaria, Hungary and Balkans"),
     ("MDE", "Middle East"),
    )

    country = models.CharField(max_length=150, blank=True)
    country_code = models.CharField(unique=True, max_length=6, blank=True)
    region = models.CharField(max_length=150, blank=True)
    region_code = models.CharField(max_length=5, blank=True)

    def __unicode__(self):
        return self.country

    @classmethod
    def get_country(cls, code):
        return Country.objects.get(country_code=code).country

    # @classmethod
    # def populate_countries(cls):
    #     """Run if country table is empty. JUST ONCE!"""
    #     countries = Player.COUNTRIES #create this first
    #     for c in countries:
    #         new = Country(country=c[1], country_code=c[0], region="changeme", region_code='ABC')
    #         new.save()

    @classmethod
    def gen_country_list(cls):
        """may never use this method but..."""
        if cache.get('country_list'):
            pass
        else:
            countries = Country.objects.all()
            cs = ()
            for c in countries:
                cs = cs + ((c.country_code, c.country))
            cache.set('country_list', cs)
        return cache.get('country_list')


class Profile(models.Model):

    avg_score = models.FloatField(null=True, blank=True, default=0, verbose_name='average score')

    def __unicode__(self):
        try:
            return self.player.user.username+"\t|\t average score: "+str(self.avg_score)
        except:
            return "profile not available for user"

    def update_avg_score(self):
        games = self.player.game_set.all()
        #print "count of the games: %d" % len(games)
        n_games = len(games)
        avg = 0
        cont = 0

        for game in games:
            avg += game.score or 0
            cont += 1

        avg_score = avg/cont

        if n_games > 1 and n_games <= 5:
            avg_score += (n_games-1)*0.5
        elif n_games > 5 and n_games <= 15:
            avg_score += 2 + (n_games-5)*0.2
        elif n_games > 15 and n_games <= 55:
            avg_score += 4 + (n_games-15)*0.1
        elif n_games > 55 and n_games <= 135:
            avg_score += 8 + (n_games-55)*0.05
        elif n_games > 135 and n_games <= 535:
            avg_score += 12 + (n_games-135)*0.01
        elif n_games > 535:
            avg_score += 16 + (n_games-535)*0.005

        self.avg_score = avg_score
        self.save()


class Player(models.Model):
    GENDER = (
     (None, '---------'),
     ('f', 'Female'),
     ('m', 'Male'),
     ('ns', "Not specified"),
    )
    AGE_RANGES = (
     (None, '---------'),
     ('18_24', '18 - 24'),
     ('25_34', '25 - 34'),
     ('35_44', '35 - 44'),
     ('45_54', '45 - 54'),
     ('55_64', '55 - 64'),
     ('more_65', '65 or more'),
    )
    EDUCATION_LEVELS = (
     (None, '---------'),
     ('ps', u'Primary school'),
     ('ss', u'Secondary school'),
     ('college', u'College degree'),
     ('bachelor', u'Bachelor degree'),
     ('master', u'Master degree'),
     ('phd', u'PhD degree'),
     ('other', u'Other'),
    )

    user = models.OneToOneField(User, unique=True, verbose_name='player') #Find out how to display as nickname!! :) MZ
    gender = models.CharField(max_length=10, blank=False, choices=GENDER, default=None, verbose_name=u'gender')
    age = models.CharField(max_length=10, blank=False, choices=AGE_RANGES, default=None, verbose_name=u'age range (years)',
                           help_text="I hereby certify that I am 18 years of age or older.")
    education = models.CharField(max_length=20, blank=False, choices=EDUCATION_LEVELS, default=None, verbose_name=u'education level')
    country = models.ForeignKey(Country, default=None, verbose_name=u'country of origin')
    profile = models.OneToOneField(Profile, unique=True, verbose_name='profile')

    def __unicode__(self):
        return self.user.username+"\t|\tfrom "+self.country.country

    #@classmethod
    #def print_countries(cls):
    #    print 'COUNTRIES = ('
    #    fl = open('countries.json')
    #    jfile = json.load(fl)
    #    for country in jfile:
    #        print "('%s', u'%s')," % (country['alpha-3'], country['name'])
    #    print ')'
