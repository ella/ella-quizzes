from django.test import TestCase
from django.core.exceptions import ValidationError

from ella_quizzes.models import Question, Quiz

from nose import tools

class TestQuestion(TestCase):
    def test_choices_get(self):
        q = Question(choices_data=Question.SEPARATOR.join(['choice 1', 'ch2', 'Uaaaaa, we are all gonna die!!!!']))

        tools.assert_equals(['choice 1', 'ch2', 'Uaaaaa, we are all gonna die!!!!'], q.choices)

    def test_choices_set(self):
        q = Question()
        q.choices = ['choice 1', 'ch2', 'Uaaaaa, we are all gonna die!!!!']

        tools.assert_equals(Question.SEPARATOR.join(['choice 1', 'ch2', 'Uaaaaa, we are all gonna die!!!!']), q.choices_data)

    def test_validation_fails_when_too_few_choices(self):
        quiz = Quiz(choices=3)

        q = Question(quiz=quiz)
        q.choices = ['just', 'two']
        tools.assert_raises(ValidationError, q.full_clean, exclude=['quiz', 'order', 'text'])

    def test_validation_fails_when_too_many_choices(self):
        quiz = Quiz(choices=1)

        q = Question(quiz=quiz)
        q.choices = ['one', 'too many']
        tools.assert_raises(ValidationError, q.full_clean, exclude=['quiz', 'order', 'text'])

    def test_validation_passes_for_correct_no_of_choices(self):
        quiz = Quiz(choices=2)

        q = Question(quiz=quiz)
        q.choices = ['just', 'right']
        q.full_clean(exclude=['quiz', 'order', 'text'])
