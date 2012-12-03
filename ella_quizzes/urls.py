from django.conf.urls.defaults import patterns, url

from ella_quizzes.views import get_result

urlpatterns = patterns('',
    url(r'^$', get_result, name='quiz-result'),
)
