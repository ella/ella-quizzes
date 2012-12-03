from django.test import TestCase

from ella_quizzes.models import Question

from nose import tools

class TestQuestion(TestCase):
    def test_choices_get(self):
        q = Question(choices_data=Question.SEPARATOR.join(['choice 1', 'ch2', 'Uaaaaa, we are all gonna die!!!!']))

        tools.assert_equals(['choice 1', 'ch2', 'Uaaaaa, we are all gonna die!!!!'], q.choices)

    def test_choices_set(self):
        q = Question()
        q.choices = ['choice 1', 'ch2', 'Uaaaaa, we are all gonna die!!!!']

        tools.assert_equals(Question.SEPARATOR.join(['choice 1', 'ch2', 'Uaaaaa, we are all gonna die!!!!']), q.choices_data)
