from django.forms.models import inlineformset_factory

from ella_quizzes.models import Quiz, Result
from ella_quizzes.forms import ResultInlineFormset

from nose import tools

from .cases import QuizTestCase

ResultFormset = inlineformset_factory(Quiz, Result, formset=ResultInlineFormset)
prefix = ResultFormset.get_default_prefix()

class TestResultFormSet(QuizTestCase):
    def setUp(self):
        super(TestResultFormSet, self).setUp()
        Result.objects.all().delete()
        self.data = {
            '%s-TOTAL_FORMS' % prefix: '4',
            '%s-INITIAL_FORMS' % prefix: '0',

            '%s-0-choice' % prefix: '0',
            '%s-0-text' % prefix: 'text 0',

            '%s-1-choice' % prefix: '1',
            '%s-1-text' % prefix: 'text 1',

            '%s-2-choice' % prefix: '2',
            '%s-2-text' % prefix: 'text 2',
        }

    def test_formset_cleans_correct_data(self):
        formset = ResultFormset(instance=self.quiz, data=self.data)

        tools.assert_true(formset.is_valid())

    def test_formset_fails_if_not_all_choices_are_covered(self):
        del self.data['%s-2-choice' % prefix]
        del self.data['%s-2-text' % prefix]
        formset = ResultFormset(instance=self.quiz, data=self.data)

        tools.assert_false(formset.is_valid())

    def test_formset_fails_if_there_are_extra_choices(self):
        self.data['%s-3-choice' % prefix] = '3'
        self.data['%s-3-text' % prefix] = 'Text 3'
        formset = ResultFormset(instance=self.quiz, data=self.data)

        tools.assert_false(formset.is_valid())

    def test_formset_fails_if_there_are_incorrect_choices(self):
        self.data['%s-0-choice' % prefix] = '4'
        formset = ResultFormset(instance=self.quiz, data=self.data)

        tools.assert_false(formset.is_valid())

    def test_formset_fails_if_there_are_duplicite_choices(self):
        self.data['%s-0-choice' % prefix] = '1'
        formset = ResultFormset(instance=self.quiz, data=self.data)

        tools.assert_false(formset.is_valid())
