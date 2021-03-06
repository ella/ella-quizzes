from django.test import TestCase
from django.core.exceptions import ValidationError

from ella_quizzes.models import Question, Quiz, Choice

from nose import tools

from .cases import QuizTestCase

class TestQuestion(TestCase):
    choices = [Choice(id=i, text=t) for (i, t) in enumerate(('choice 1', 'ch2', 'Uaaaaa, we are all gonna die!!!!'))]

    def test_choices_get(self):
        q = Question(choices_data=Question.SEPARATOR.join(['choice 1', 'ch2', 'Uaaaaa, we are all gonna die!!!!']))

        tools.assert_equals(self.choices, q.choices)

    def test_choices_set(self):
        q = Question()
        q.choices = self.choices

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

class TestQuiz(QuizTestCase):
    def test_get_returns_result_for_top_choice(self):
        tools.assert_equals(self.results[1], self.quiz.get_result(['0', '1', '1']))

    def test_validate_choices_passes_for_valid_choices(self):
        choices = ['0', '1', '1']
        tools.assert_equals(map(int, choices), self.quiz.clean_choices(choices))

    def test_validate_choices_fails_for_incorrect_choice_count(self):
        choices = ['0', '1', '1', '2']
        tools.assert_raises(ValidationError, self.quiz.clean_choices, choices)

    def test_validate_choices_fails_for_incorrect_choice_type(self):
        choices = ['0', '1', '']
        tools.assert_raises(ValidationError, self.quiz.clean_choices, choices)

    def test_validate_choices_fails_for_incorect_choice_value(self):
        choices = ['0', '1', '11']
        tools.assert_raises(ValidationError, self.quiz.clean_choices, choices)
