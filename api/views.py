from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from accounts.serializers import UserSerializer
from tms.serializers import TaskSerializer, TaskDetailSerializer
from tms.models import Task
from crypter.crypto import PasswordHasher, TextHasher
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

# Account section

class MeView(APIView):
    """Return information about logged in user"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Supports only GET metgod"""

        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class MyTasksView(ListAPIView):
    """
    Return tasks from current user
    Uses ListAPIView for better output
    Also guarantee better filtration/pagination (in the future)
    """

    serializer_class = TaskDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pk = self.request.user.id
        return Task.objects.filter(author_id=pk)

# Task section

class TaskViewSet(ModelViewSet):
    """Task View Set"""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Create query set using some permissions"""

        if self.request.user.is_superuser:
            return Task.objects.all()

        return Task.objects.filter(author=self.request.user)

    def perform_save(self, serializer):
        password = self.request.data.get('password')
        text = serializer.validated_data.get('text')

        if password and text:
            hashed_pass = PasswordHasher(password).hash_password()
            encrypted_text = TextHasher(password).encrypt(text)

            serializer.save(
                author=self.request.user,
                password=hashed_pass,
                text=encrypted_text
            )
        else:
            serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Update task via PUT/PATCH using perform_save function as DRY principle"""

        self.perform_save(serializer=serializer)

    def perform_create(self, serializer):
        """Create task via POST using perform_save function as DRY principle"""

        self.perform_save(serializer)

# Admin section

# User section

class GetUserInfo(RetrieveAPIView):
    """Return user info by ID (Only admins allowed)"""

    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "pk"

# Task section

class GetUserTasks(ListAPIView):
    """
    Return tasks from user by ID (Only admins allowed)
    Uses ListAPIView for better output
    """

    serializer_class = TaskDetailSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        """Query set by ID"""

        pk = self.kwargs['pk']
        return Task.objects.filter(author_id=pk)
