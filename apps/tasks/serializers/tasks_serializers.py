from rest_framework.serializers import ModelSerializer

from apps.tasks.models import Task


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "title", "description", "completed", "created_at", "updated_at")
        read_only_fields = ["id", "created_at", "updated_at"]
