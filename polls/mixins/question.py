from django.http import Http404

from polls.models.choice import Choice
from polls.models.question import Question


class QuestionMixin(object):
    def get_question_obj(self, id):
        try:
            return Question.objects.get(id=id)
        except Question.DoesNotExist:
            raise Http404

    def get_choice_obj(self, question, choice_id):
        try:
            return question.choices.get(id=choice_id)
        except Choice.DoesNotExist:
            raise Http404
