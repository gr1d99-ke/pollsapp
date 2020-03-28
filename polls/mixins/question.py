from django.http import Http404

from tenants.utils import tenant_from_request

from polls.models.choice import Choice
from polls.models.question import Question


class QuestionMixin(object):
    def get_question_obj(self, request, id):
        try:
            tenant = tenant_from_request(request)
            return Question.objects.filter(tenant=tenant).get(id=id)
        except Question.DoesNotExist:
            raise Http404

    def get_choice_obj(self, request, question, choice_id):
        try:
            tenant = tenant_from_request(request)
            return question.choices.filter(tenant=tenant).get(id=choice_id)
        except Choice.DoesNotExist:
            raise Http404
