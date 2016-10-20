from django.contrib import admin
from models import Question, Game, AnsweredQuestion

# Register your models here.
admin.site.register(Question)
admin.site.register(Game)
admin.site.register(AnsweredQuestion)