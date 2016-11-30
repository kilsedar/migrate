# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import calendar
import re
import random
import ast
from django.db import models
from django.db.models.fields.related import ManyToManyField
from django.db.models import Q
from utils import *
from players.models import Country, Player

# Create your models here.
class Question(models.Model):
    TYPES = (("MC", "Multiple choice"),
             ("TB", "Text-based"),
             ("TF", "True or False"),
             ("MB", "Map based"),
             )

    ANSWER_TYPES = (("NUM", "Numeric"),
                    ("FIX", "Fixed"),
                    ("CNT", "Country"),
                    ("PER", "Percentage"),
                    ("CLR", "Date Range"),
                    ("BOL", "Boolean"),
                    ("ALP", "Alphabetic or other"),
                    ("MON", "Month(s)"),
                    )

    category = models.CharField(max_length=50, blank=True, verbose_name="categories")
    region = models.CharField(max_length=120, blank=True, null=True)
    _type = models.CharField(blank=True, null=False, max_length=4, choices=TYPES, verbose_name='type')
    question = models.TextField(blank=True, verbose_name='question')
    answer = models.TextField(blank=True, verbose_name='right answer')
    answer_type = models.CharField(max_length=4, blank=True, null=True, default="ALP", verbose_name='answer type')
    random_factor = models.IntegerField(null=True, blank=True)
    help_text = models.TextField(blank=True)
    data_source = models.CharField(max_length=200, blank=True)
    data_source_link = models.CharField(max_length=500, blank=True)
    license_link = models.CharField(max_length=500, blank=True)
    cnt_list = models.CharField(max_length=599, blank=True)


    def __unicode__(self):
        return self.question + "\t|\tAnswer: " + self.answer + "\t|\t(" + self._type + ")"

    def to_dict(self):
        opts = self._meta
        data = {}
        for f in opts.concrete_fields + opts.many_to_many:
            if isinstance(f, ManyToManyField):
                if self.pk is None:
                    data[f.name] = []
                else:
                    data[f.name] = list(f.value_from_object(self).values_list('pk', flat=True))
            else:
                data[f.name] = f.value_from_object(self)
            if self._type == 'MB' and self.answer_type == 'MB':
                data['answer_code'] = self.answer_code
        return data

    @property
    def answer_code(self):
        if self._type == 'MB':
            return ast.literal_eval(self.cnt_list)[0]
        return self.answer

    @classmethod
    def get_question(cls, type, category, region):
        """Method to filter questions"""
        if (region != ""):
            qs_list = Question.objects.filter(_type=type, category=category, region=region).values_list('id', flat=True)
        else:
            qs_list = Question.objects.filter(_type=type, category=category).values_list('id', flat=True)
        qs_id = random.choice(qs_list)
        qs = Question.objects.filter(id=qs_id)[0]
        return qs

    @classmethod
    def get_questions(cls, country):
        questionnaire = list()

        #user region & text-based
        region = country.region
        if region == 'changeme':
            region = 'Europe'
        questionnaire.append(cls.get_question("TB", "USER REGION", region.upper()))

        #user region & multiple-choice
        questionnaire.append(cls.get_question("MC", "USER REGION", region.upper()))

        #mediterranean & map-based
        questionnaire.append(cls.get_question("MB", "MEDITERRANEAN AREA", ""))

        #mediterranean & multiple-choice
        questionnaire.append(cls.get_question("MC", "MEDITERRANEAN AREA", ""))

        #general overview & true-false
        questionnaire.append(cls.get_question("TF", "GENERAL OVERVIEW", ""))

        #general overview & map-based
        questionnaire.append(cls.get_question("MB", "GENERAL OVERVIEW", ""))

        random.shuffle(questionnaire)
        return questionnaire

    def get_mix_answers(self):
        """Generates fake answers and mixes it with the right one. USE THIS ONE EYLUL!"""
        _all = self.get_answers() # + self.answer
        random.shuffle(_all)
        return _all

    def get_context_num(self):
        """Returns a tuple with the begining and end of a numeric answer"""
        found = re.search('\d+', self.answer)
        if found:
            start = found.start()
            end = found.end()
            return (self.answer[0:start], self.answer[end:])
        else:
            return ("", "")

    def get_answers(self):
        """According to answer_type generates 3 random fake answers and adds the real one"""
        if self.answer_type == "MON":
            """Generates options for answers that a months of the year"""
            if self.random_factor:
                return get_rnd_months(self.answer, rf = self.random_factor) + [self.answer]
            return get_rnd_months(self.answer) + [self.answer]

        if self.answer_type == "NUM":
            """Generate options based on random numbers"""
            ans = list()
            context = self.get_context_num()
            ans.append(self.answer) #right answer

            r = round(0.9999999-random.random(), 2)
            op = int(r * self.random_factor)
            found = re.search('\d+', self.answer)
            if found:
                answer = int(self.answer[found.start():found.end()])

            while too_close(answer, op) == True or context[0]+str(op)+context[1] in ans:
                r = round(0.9999999-random.random(), 2)
                op = int(r * self.random_factor)
            ans.append(context[0]+str(op)+context[1])

            for i in range(2):
                while too_close(answer, op) == True or context[0]+str(op)+context[1] in ans:
                    r = round(0.9999999-random.random(), 2)
                    x = 0.1 if r > 0.5 else 10
                    op = int(r * self.random_factor * x)
                ans.append(context[0]+str(op)+context[1])

            return ans

        if self.answer_type == "FIX" and self._type != 'MB':
            """If the answer is fixed but not a country"""
            if not self.fixedanswers:
                print self
            return [self.answer,
                    self.fixedanswers.option2,
                    self.fixedanswers.option3,
                    self.fixedanswers.option4]
        elif self._type == 'MB':
            """If the the answer is a country"""
            try:
                l = ast.literal_eval(self.cnt_list)
                if len(l) > 4:
                    answer = l[0]
                    random.shuffle(l)
                    while (answer in l[:3]):
                        shuffle(l)
                    return [answer]+l[:3]
                else:
                    return l
            except Exception, e:
                print self
                print str(e)
        if self.answer_type == "PER":
            """Generates option when the answer is a percentage"""
            bef, aft = self.get_context_num()
            pos = [10, 20, 30, 40, 50, 60, 70, 80, 90]

            while self.answer in pos[:3]:
                random.shuffle(pos)

            return [self.answer] + [ bef+str(per)+aft for per in pos[:3]]
        return["temp", "temp", "temp", "temp"]

    def check_TB_answer(self, num):
        """Method to check if the answer provided by the user if +-20% far
        from the real answer"""
        try:
            num = int(num)
            rng = (ans*20/100)
            if (ans-rng)<num<(ans+rng):
                return True
            return False
        except:
            print "not a number! (int)"
            return False


class FixedAnswers(models.Model):

    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    option2 = models.TextField(blank=True, verbose_name='option 2')
    option3 = models.TextField(blank=True, verbose_name='option 3')
    option4 = models.TextField(blank=True, verbose_name='option 4')

    def __unicode__(self):
        return self.question.question

class Game(models.Model):

    player = models.ForeignKey(Player)
    score = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __unicode__(self):
        return self.player.user.username+"\t|\tscored:"+str(self.score)+"\t|\t"+self.date.strftime("%d/%m/%Y")+" at: "+self.date.strftime("%H:%M")

class AnsweredQuestion(models.Model):

    question = models.ForeignKey(Question)
    user_answer = models.TextField(blank=True, verbose_name='user answer')
    option1 = models.TextField(blank=True, null=True, verbose_name='option 1')
    option2 = models.TextField(blank=True, null=True, verbose_name='option 2')
    option3 = models.TextField(blank=True, null=True, verbose_name='option 3')
    option4 = models.TextField(blank=True, null=True, verbose_name='option 4')
    game = models.ForeignKey(Game)


    def __unicode__(self):
        return self.question.question+" "+self.user_answer
