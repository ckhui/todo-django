from rest_framework import serializers
from .models import Task


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "title", "date_created", "completed")

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.completed = validated_data.get("completed", instance.completed)
        instance.save()
        return instance