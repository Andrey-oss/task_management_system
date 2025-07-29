from rest_framework import serializers
from tms.models import Task
from accounts.serializers import UserMiniSerializer

class TaskSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    password = serializers.CharField(write_only=True, required=False) # You can't read the password hash

    class Meta:
        model = Task
        fields = ['id', 'title', 'text', 'status', 'created_at', 'edited_at', 'deadline', 'image', 'password', 'author_name']
        read_only_fields = ['id', 'created_at', 'edited_at']

class TaskDetailSerializer(serializers.ModelSerializer):
    author = UserMiniSerializer(read_only=True)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Task
        fields = ['id', 'title', 'text', 'status', 'created_at', 'edited_at', 'deadline', 'image', 'password', 'author']
        read_only_fields = fields
