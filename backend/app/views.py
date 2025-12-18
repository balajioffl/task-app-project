from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Task
from .serializers import TaskSerializer
from .permissions import hasAccess

@api_view(["GET"])
def check(request):
    return Response({"msg": "backend is working !"})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def test_api(request):

    return Response(
    {
        "msg": "JWT is working !",
        "user": request.user.username
    })


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, hasAccess]

    def get_queryset(self):
        user = self.request.user

        if user.profile.role and user.profile.role.name == "Admin":
            return Task.objects.all()

        return Task.objects.filter(created_by=user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_role(request):

    profile = request.user.profile

    return Response(
    {
        "username": request.user.username,
        "role": profile.role.name if profile.role else None
    })
