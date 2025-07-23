from rest_framework import serializers
from accounts.serializers import UserSerializer
from tms.models import Task

class TaskSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'author_name', 'text', 'status', 'category']
