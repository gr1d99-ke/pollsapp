from django.db.models import F

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from polls.mixins.question import QuestionMixin
from polls.models.question import Question
from polls.api.serializers.question import QuestionSerializer
from polls.api.serializers.choice import ChoiceSerializer


class QuestionView(APIView):
    """
    List all `Questions` or Create a new `Question`
    """

    def get(self, request, format=None):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = QuestionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetailView(QuestionMixin, APIView):
    """
    Retrieve, Update or Destroy a Question
    """

    def get(self, request, id, format=None):
        question = self.get_question_obj(id)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        question = self.get_question_obj(id)
        serializer = QuestionSerializer(question, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        question = self.get_question_obj(id)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionChoicesView(QuestionMixin, APIView):
    """
    List all `Choices` for a `Question` or Create a new `Choice`
    """

    def get(self, request, id, format=None):
        question = self.get_question_obj(id)
        choices = question.choices.all()
        serializer = ChoiceSerializer(choices, many=True)
        return Response(serializer.data)

    def post(self, request, id, format=None):
        question = self.get_question_obj(id)
        serializer = ChoiceSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(question=question)

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionChoicesDetailView(QuestionMixin, APIView):
    """
    Retrieve, Update or Destroy a `Question` `Choice`
    """

    def get(self, request, id, choice_id, format=None):
        question = self.get_question_obj(id)
        choice = self.get_choice_obj(question, choice_id)
        serializer = ChoiceSerializer(choice)
        return Response(serializer.data)

    def put(self, request, id, choice_id, format=None):
        question = self.get_question_obj(id)
        choice = self.get_choice_obj(question, choice_id)
        serializer = ChoiceSerializer(choice, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, choice_id, format=None):
        question = self.get_question_obj(id)
        choice = self.get_choice_obj(question, choice_id)
        choice.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VotesView(QuestionMixin, APIView):
    """
    Vote for a specific `Choice`
    """

    def put(self, request, id, choice_id, format=None):
        question = self.get_question_obj(id)
        choice = self.get_choice_obj(question, choice_id)
        choice.votes = F('votes') + 1 # a
        choice.save()
        choice.refresh_from_db()
        serializer = ChoiceSerializer(choice)
        return Response(serializer.data)
