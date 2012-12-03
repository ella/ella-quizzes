from django.test import TestCase
from django.core.exceptions import ValidationError

from ella.utils.test_helpers import create_basic_categories
from ella.utils.timezone import now

from ella_quizzes.models import Question, Quiz, Result, Choice

from nose import tools

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

class TestQuiz(TestCase):
    def setUp(self):
        super(TestQuiz, self).setUp()
        create_basic_categories(self)
        self.quiz = Quiz.objects.create(
                title=u'First Quiz',
                slug=u'first-quiz',
                description=u'First quiz',
                category=self.category_nested,
                publish_from=now(),
                published=True,

                intro_title='Answer me!',
                intro_text='Some even longer test. \n' * 5,
                choices=3
        )
        self.results = [
            Result.objects.create(
                quiz=self.quiz,
                choice=ch,
                text='You chose %d' % ch
            ) for ch in range(3)
        ]
        self.questions = [
            Question.objects.create(
                quiz=self.quiz,
                order=x,
                text='WTF %d?!' % x,
                choices_data=Question.SEPARATOR.join('%d FTW!' % ch for ch in range(3))
            ) for x in range(3)
        ]

    def test_get_returns_result_for_top_choice(self):
        tools.assert_equals(self.results[1], self.quiz.get_result(['0', '1', '1']))
