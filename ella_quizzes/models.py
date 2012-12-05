from collections import Counter, namedtuple
from operator import itemgetter

from django.db import models
from django.core.exceptions import ValidationError

from app_data import AppDataField

from ella.core.models import Publishable
from ella.photos.models import Photo
from ella.core.cache import CachedForeignKey, cache_this


class Quiz(Publishable):
    intro_title = models.CharField(max_length=200)
    intro_text = models.TextField()

    choices = models.PositiveIntegerField(help_text='Number of choices for every question.')

    @property
    @cache_this(lambda q: 'quiz_questions:%s' % q.id)
    def questions(self):
        return list(self.question_set.order_by('order'))

    @property
    @cache_this(lambda q: 'quiz_results:%s' % q.id)
    def results(self):
        return dict((r.choice, r) for r in self.result_set.all())

    def clean_choices(self, choices):
        try:
            choices = map(int, choices)
        except ValueError:
            raise ValidationError('Choices must be integers!')

        if len(choices) != len(self.questions):
            raise ValidationError('There must be an answer for every question')

        if min(choices) < 0 or max(choices) >= self.choices:
            raise ValidationError('incorrect choice!')

        # TODO: convert to Choice objects?
        return choices

    def get_result(self, choices):
        top_choice = sorted(Counter(choices).items(), key=itemgetter(1), reverse=True)[0][0]
        return self.results[int(top_choice)]

class Result(models.Model):
    quiz = CachedForeignKey(Quiz)
    choice = models.IntegerField()

    photo = CachedForeignKey(Photo, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    text = models.TextField()

    # generic JSON field to store app specific data
    app_data = AppDataField(default='{}', editable=False)

    class Meta:
        unique_together = (('quiz', 'choice', ), )

# forwards-compatible wrapper around individual choices for a question
Choice = namedtuple('Choice', 'id text')

class Question(models.Model):
    SEPARATOR = '\x01'

    quiz = CachedForeignKey(Quiz)
    order = models.PositiveIntegerField()

    photo = CachedForeignKey(Photo, blank=True, null=True, on_delete=models.SET_NULL)
    text = models.TextField()

    choices_data = models.TextField()

    class Meta:
        unique_together = (('quiz', 'order', ), )

    def clean(self):
        if len(self.choices) != self.quiz.choices:
            raise ValidationError('Number of choices must match the Quiz.')

    def get_choices(self):
        # TODO: maybe a SortedDict would be better?
        return map(lambda ch: Choice(*ch), enumerate(self.choices_data.split(self.SEPARATOR)))

    def set_choices(self, choices):
        self.choices_data = self.SEPARATOR.join(map(itemgetter(1), sorted(choices)))
    choices = property(get_choices, set_choices)
