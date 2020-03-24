from django.http import Http404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models.question import Question
from .serializers import QuestionSerializer


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


class QuestionDetailView(APIView):
    """
    Retrieve, Update or Destroy a Question
    """
    def get_object(self, id):
        try:
            return Question.objects.get(id=id)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        question = self.get_object(id)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def put(self, request, id, format=None):
      question = self.get_object(id)
      serializer = QuestionSerializer(question, data=request.data)

      if serializer.is_valid():
          serializer.save()
          return Response(serializer.data)

      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        question = self.get_object(id)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
