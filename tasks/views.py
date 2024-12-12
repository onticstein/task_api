from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Task
from .serializers import TaskSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['patch'], url_path='complete')
    def complete(self, request, pk=None):
        task = self.get_object()
        if not task.completed:
            task.completed = True
            task.save()
            return Response({'status': 'Task marked as completed'}, status=status.HTTP_200_OK)
        return Response({'error': 'Task is already completed'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], url_path='uncomplete')
    def uncomplete(self, request, pk=None):
        task = self.get_object()
        if task.completed:
            task.completed = False
            task.save()
            return Response({'status': 'Task marked as not completed'}, status=status.HTTP_200_OK)
        return Response({'error': 'Task is not completed'}, status=status.HTTP_400_BAD_REQUEST)