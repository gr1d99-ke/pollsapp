from rest_framework import serializers

from polls.models.choice import Choice


class ChoiceSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    choice_text = serializers.CharField(max_length=200)
    votes = serializers.IntegerField(default=0, required=False)

    def create(self, validated_data):
        return Choice.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.choice_text = validated_data.get('choice_text', instance.choice_text)
        instance.save()
        return instance
