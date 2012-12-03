from django.test import TestCase

from ella.utils.test_helpers import create_basic_categories
from ella.utils.timezone import now

from ella_quizzes.models import Question, Quiz, Result

class QuizTestCase(TestCase):
    def setUp(self):
        super(QuizTestCase, self).setUp()
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

