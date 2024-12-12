from rest_framework import serializers
from .models import Task
from rest_framework.reverse import reverse

class TaskSerializer(serializers.ModelSerializer):
    actions = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'completed', 'created_by', 'created_at', 'actions']
        read_only_fields = ['created_by', 'created_at']

    def get_actions(self, obj):
        request = self.context.get('request')
        actions = {}

        if not obj.completed:
            actions['complete'] = {
                'url': reverse('task-complete', kwargs={'pk': obj.pk}, request=request),
                'method': 'PATCH',
                'description': 'Mark this task as completed'
            }
        else:
            actions['uncomplete'] = {
                'url': reverse('task-uncomplete', kwargs={'pk': obj.pk}, request=request),
                'method': 'PATCH',
                'description': 'Mark this task as not completed'
            }

        return actions