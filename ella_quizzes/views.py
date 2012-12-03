from django.template.response import TemplateResponse
from django.http import HttpResponseBadRequest
from django.views.decorators.http import require_POST

from ella.core.views import get_templates_from_publishable

@require_POST
def get_result(request, context):
    choices = request.POST.get('choices', [])
    quiz = context['object']
    if not quiz.validate_choices(choices):
        return HttpResponseBadRequest()

    context['result'] = quiz.get_result(choices)

    template_name = 'quiz_result.html'
    if request.is_ajax():
        template_name = 'quiz_result_async.html'
    return TemplateResponse(request, get_templates_from_publishable(quiz, template_name), context)
