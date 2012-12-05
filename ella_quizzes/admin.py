from django.contrib import admin

from ella_quizzes.models import Quiz, Result, Question
from ella_quizzes.forms import ResultInlineFormset

class ResultInline(admin.TabularInline):
    model = Result
    formset = ResultInlineFormset
    raw_id_fields = ('photo',)

class QuestionInline(admin.TabularInline):
    model = Question
    raw_id_fields = ('photo',)

class QuizModelAdmin(admin.ModelAdmin):
    inlines = [ResultInline, QuestionInline]
    raw_id_fields = ('photo',)

admin.site.register(Quiz, QuizModelAdmin)
