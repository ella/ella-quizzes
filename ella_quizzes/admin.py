from django.contrib import admin

from ella_quizzes.models import Quiz, Result, Question
from ella_quizzes.forms import ResultInlineFormset

class ResultInline(admin.TabularInline):
    model = Result
    formset = ResultInlineFormset

class QuestionInline(admin.TabularInline):
    model = Question

class QuizModelAdmin(admin.ModelAdmin):
    inlines = [ResultInline, QuestionInline]

admin.site.register(Quiz, QuizModelAdmin)
