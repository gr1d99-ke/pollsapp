from rest_framework import serializers

from .models.question import Question


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    question_text = serializers.CharField(max_length=200)
    pub_date = serializers.DateTimeField()

    def create(self, validated_data):
        """
        Create and return a new `Question` instance, given the validated data
        :param validated_data:
        :return:
        """

        return Question.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return existing `Question` instance, given validated data
        :param instance:
        :param validated_data:
        :return:
        """
        instance.question_text = validated_data.get('question_text', instance.question_text)
        instance.pub_date = validated_data.get('pub_date', instance.pub_date)
        return instance
