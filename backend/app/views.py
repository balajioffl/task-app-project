from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django.core.exceptions import PermissionDenied
from .models import Task
from .serializers import TaskSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .pagination import TaskPagination
from rest_framework.filters import SearchFilter


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
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = TaskPagination
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']


    def get_queryset(self):
        
        user = self.request.user

        if user.groups.filter(name="Admin").exists():
            return Task.objects.all()
        
        return Task.objects.filter(created_by=user)


    def perform_create(self, serializer):

        serializer.save(created_by=self.request.user)


    def perform_update(self,serializer):

        user = self.request.user

        if user.groups.filter(name="Admin").exists():
            serializer.save()

        else:
            if serializer.instance.created_by == user:
                serializer.save()

            else:
                raise PermissionDenied("You can only edit your own task !")
            
        
    def perform_destroy(self, instance):
        
        user = self.request.user

        if user.groups.filter(name="Admin").exists():
            instance.delete()

        else:
            if instance.created_by == user:
                instance.delete()

            else:
                raise PermissionDenied("You can only delete your own task only !")
            
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_groups(request):
    
    return Response({
        "username": request.user.username,
        "groups": list(request.user.groups.values_list("name", flat=True))
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile(request):
    return Response({
        "username": request.user.username,
    })
