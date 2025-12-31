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
from django.core.cache import cache
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


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
    

    def list(self, request, *args, **kwargs):

        user = request.user
        is_admin = user.groups.filter(name="Admin").exists()

        cache_key = "tasks_list_admin" if is_admin else f"tasks_list_user_{user.id}"
        cached_data = cache.get(cache_key)

        if cached_data:

            logger.info("Task cache Hit")
            print("Cache Hit")
            return Response(cached_data)
        
        logger.info("Task cache hit miss")
        print("Task cache hit miss")

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60)

        return response


    def perform_create(self, serializer):

        serializer.save(created_by=self.request.user)

        cache.delete("tasks_list_admin")
        cache.delete(f"tasks_list_user_{self.request.user.id}")

        print("Cache cleared after task create")


    def perform_update(self,serializer):

        user = self.request.user

        if user.groups.filter(name="Admin").exists():
            serializer.save()

        else:
            if serializer.instance.created_by == user:
                serializer.save()

            else:
                raise PermissionDenied("You can only edit your own task !")

        cache.delete("tasks_list_admin")
        cache.delete(f"tasks_list_user_{serializer.instance.created_by.id}")

        print("Cache cleared after task update")
            
        
    def perform_destroy(self, instance):
        
        user = self.request.user

        if user.groups.filter(name="Admin").exists():
            instance.delete()

        else:
            if instance.created_by == user:
                instance.delete()

            else:
                raise PermissionDenied("You can only delete your own task only !")
            
        cache.delete("tasks_list_admin")
        cache.delete(f"tasks_list_user_{instance.created_by.id}")

        print("Cache cleared after task delete")
            
    
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


