from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from accounts.serializers import UserSerializer
from tms.serializers import TaskSerializer
from tms.models import Task

# Account section

class MeView(APIView):
    """Return information about logged in user"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Supports only GET metgod"""

        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Create query set using some permissions"""
        if self.request.user.is_superuser:
            return Task.objects.all()

        return Task.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
