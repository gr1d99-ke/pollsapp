from django.db.models import F

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from tenants.mixins import TenantMixin
from tenants.utils import tenant_from_request

from polls.mixins.question import QuestionMixin
from polls.models.question import Question
from polls.api.serializers.question import QuestionSerializer
from polls.api.serializers.choice import ChoiceSerializer


class QuestionView(TenantMixin, APIView):
    """
    List all `Questions` or Create a new `Question`
    """

    permission_classes = [IsAuthenticated, ]

    def get(self, request, format=None):
        tenant = self.get_tenant(request)
        questions = Question.objects.filter(tenant=tenant)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = QuestionSerializer(data=request.data)

        if serializer.is_valid():
            tenant = self.get_tenant(request)
            serializer.save(tenant=tenant)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetailView(QuestionMixin, APIView):
    """
    Retrieve, Update or Destroy a Question
    """

    permission_classes = [IsAuthenticated, ]

    def get(self, request, id, format=None):
        question = self.get_question_obj(request, id)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        question = self.get_question_obj(request, id)
        serializer = QuestionSerializer(question, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        question = self.get_question_obj(request, id)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionChoicesView(QuestionMixin, TenantMixin ,APIView):
    """
    List all `Choices` for a `Question` or Create a new `Choice`
    """

    permission_classes = [IsAuthenticated, ]

    def get(self, request, id, format=None):
        tenant = self.get_tenant(request)
        question = self.get_question_obj(request, id)
        choices = question.choices.filter(tenant=tenant)
        serializer = ChoiceSerializer(choices, many=True)
        return Response(serializer.data)

    def post(self, request, id, format=None):
        tenant = self.get_tenant(request)
        question = self.get_question_obj(request, id)
        serializer = ChoiceSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(question=question, tenant=tenant)

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionChoicesDetailView(QuestionMixin, APIView):
    """
    Retrieve, Update or Destroy a `Question` `Choice`
    """
    permission_classes = [IsAuthenticated, ]

    def get(self, request, id, choice_id, format=None):
        question = self.get_question_obj(request, id)
        choice = self.get_choice_obj(request, question, choice_id)
        serializer = ChoiceSerializer(choice)
        return Response(serializer.data)

    def put(self, request, id, choice_id, format=None):
        question = self.get_question_obj(request, id)
        choice = self.get_choice_obj(request, question, choice_id)
        serializer = ChoiceSerializer(choice, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, choice_id, format=None):
        question = self.get_question_obj(request, id)
        choice = self.get_choice_obj(request, question, choice_id)
        choice.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VotesView(QuestionMixin, APIView):
    """
    Vote for a specific `Choice`
    """

    permission_classes = [IsAuthenticated, ]

    def put(self, request, id, choice_id, format=None):
        question = self.get_question_obj(request, id)
        choice = self.get_choice_obj(request, question, choice_id)
        choice.votes = F('votes') + 1 # a
        choice.save()
        choice.refresh_from_db()
        serializer = ChoiceSerializer(choice)
        return Response(serializer.data)
