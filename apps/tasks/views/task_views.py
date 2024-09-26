from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.tasks.models import Task
from apps.tasks.pagination import CustomPagination
from apps.tasks.serializers.tasks_serializers import TaskSerializer


class TaskListCreateView(ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated,]
    pagination_class = CustomPagination

    @extend_schema(tags=["Tasks"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=["Tasks"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)  # Only return tasks for the authenticated user

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Save the task with the current user


# Retrieve, Update, and Delete Task
class TaskDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated,]

    @extend_schema(tags=["Tasks"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=["Tasks"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(tags=["Tasks"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(tags=["Tasks"])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
