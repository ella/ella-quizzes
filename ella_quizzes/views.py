from django.template.response import TemplateResponse
from django.http import HttpResponseBadRequest, HttpResponseRedirect, Http404
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError

from ella.core.views import get_templates_from_publishable

@require_POST
def calculate(request, context):
    choices = request.POST.getlist('choices')
    quiz = context['object']

    try:
        choices = quiz.clean_choices(choices)
    except ValidationError, e:
        return HttpResponseBadRequest(e.message)

    result = quiz.get_result(choices)
    return HttpResponseRedirect(result.get_absolute_url())

def get_result(request, context, choice):
    quiz = context['object']
    try:
        context['result'] = quiz.results[int(choice)]
    except KeyError:
        raise Http404()

    template_name = 'quiz_result.html'
    if request.is_ajax():
        template_name = 'quiz_result_async.html'
    return TemplateResponse(request, get_templates_from_publishable(template_name, quiz), context)
