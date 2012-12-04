from django.test.client import RequestFactory

from ella_quizzes.views import get_result

from nose import tools

from .cases import QuizTestCase

class TestResulView(QuizTestCase):
    def setUp(self):
        super(TestResulView, self).setUp()
        self.rf = RequestFactory()
        self.context = {'object': self.quiz}
        self.url = self.quiz.get_absolute_url() + 'results/'

    def test_correct_result_gets_rendered(self):
        request = self.rf.post(self.url, {'choices': ['0', '1', '1']})

        response = get_result(request, self.context)
        tools.assert_equals(self.results[1], response.context_data['result'])

    def test_bad_request_on_incorrect_choices(self):
        response = self.client.post(self.url, {'choices': ['0', '1', 'X']})

        tools.assert_equals(400, response.status_code)
