from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView
from .models import Task, Profile
from django.db.models import Q
from django.contrib.auth.models import User
from .serializers import TaskSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .pagination import TaskPagination
from .filters import TaskFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.core.cache import cache
from django.conf import settings
import logging
from .tasks import task_activity_log, send_task_assigned_email
import csv
from django.http import HttpResponse
from reportlab.pdfgen import canvas
import os
from django.core.mail import send_mail
from celery import shared_task


logger = logging.getLogger(__name__)


@api_view(["GET"])
def check(request):
    return Response({"msg": "backend is working !"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def test_api(request):

    return Response({"msg": "JWT is working !", "user": request.user.username})


class TaskViewSet(ModelViewSet):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    parser_classes = [MultiPartParser, FormParser]
    pagination_class = TaskPagination

    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = TaskFilter
    search_fields = ["title", "description"]

    def get_queryset(self):

        user = self.request.user

        if user.groups.filter(name="Admin").exists():
            return Task.objects.all()

        elif user.groups.filter(name="Member").exists():
            return Task.objects.filter(Q(created_by=user) | Q(assigned_to=user))

        else:
            return Task.objects.filter(created_by=user)

    def list(self, request, *args, **kwargs):

        user = request.user
        is_admin = user.groups.filter(name="Admin").exists()

        query_string = request.META.get("QUERY_STRING", "")

        cache_key = (
            f"tasks_admin_{query_string}"
            if is_admin
            else f"tasks_user_{user.id}_{query_string}"
        )
        cached_data = cache.get(cache_key)

        if cached_data:
            print("Cache Hit")
            return Response(cached_data)

        print("Cache Miss")

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60)

        return response

    def perform_create(self, serializer):

        user = self.request.user

        if user.groups.filter(name__in=["Admin", "Manager"]).exists():

            task = serializer.save(created_by=user)

            task_activity_log.delay(task.id, "CREATED", self.request.user.username)

            if task.assigned_to:
                send_task_assigned_email.delay(
                    task.assigned_to.email, task.title, user.username
                )

            cache.clear()

            print("Cache cleared after task create")

        else:
            raise PermissionDenied("You can only view tasks!")

    def perform_update(self, serializer):

        user = self.request.user
        task = serializer.instance
        old_assigned_to = task.assigned_to

        if user.groups.filter(name="Admin").exists():
            updated_task = serializer.save()

        elif user.groups.filter(name="Manager").exists():

            if task.created_by == user or task.assigned_to == user:
                updated_task = serializer.save()
            else:
                raise PermissionDenied(
                    "Managers can only edit tasks they created or are assigned to!"
                )

        else:
            raise PermissionDenied("Members cannot edit tasks!")

        task_activity_log.delay(task.id, "UPDATED", user.username)

        if updated_task.assigned_to and updated_task.assigned_to != old_assigned_to:

            send_task_assigned_email.delay(
                updated_task.assigned_to.email, updated_task.title, user.username
            )

        cache.clear()

        print("Cache cleared after task update")

    def perform_destroy(self, instance):

        user = self.request.user
        task_id = instance.id

        if user.groups.filter(name="Admin").exists():
            instance.delete()

        else:
            raise PermissionDenied("Only Admin can delete tasks !")

        task_activity_log.delay(task_id, "DELETED", user.username)

        cache.clear()

        print("Cache cleared after task delete")


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_groups(request):

    return Response(
        {
            "username": request.user.username,
            "groups": list(request.user.groups.values_list("name", flat=True)),
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile(request):
    return Response(
        {
            "username": request.user.username,
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_list(request):
    users = User.objects.all().values("id", "username")
    return Response(users)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def export_csv(request):

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="tasks.csv"'

    writer = csv.writer(response)
    writer.writerow(["ID", "Title", "Status", "Priority"])

    for task in Task.objects.all():
        writer.writerow(["ID", "Title", "Status", "Priority"])

    return response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def export_pdf(request):

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="tasks.pdf"'

    p = canvas.Canvas(response)
    y = 800

    for task in Task.objects.all():

        p.setFont("Helvetica-Bold", 10)

        p.drawString(50, y, f"Title: {task.title}")
        y -= 15

        p.setFont("Helvetica", 9)

        p.drawString(70, y, f"Status: {task.status}")
        y -= 15

        p.drawString(70, y, f"Priority: {task.priority}")
        y -= 15

        p.drawString(70, y, f"Due Date: {task.due_date if task.due_date else 'N/A'}")
        y -= 10

        p.line(50, y, 550, y)
        y -= 20

        if y < 80:
            p.showPage()
            y = 800

    p.save()
    return response


class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        profile, created = Profile.objects.get_or_create(user=request.user)

        return Response(
            {
                "username": request.user.username,
                "bio_pic": profile.bio_pic.url if profile.bio_pic else None,
            }
        )


class ProfileUpdate(APIView):

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request):

        profile, _ = Profile.objects.get_or_create(user=request.user)

        if "bio_pic" not in request.data:
            return Response({"error": "bio_pic required"}, status=400)

        profile.bio_pic = request.data["bio_pic"]
        profile.save()

        return Response({"bio_pic": profile.bio_pic.url})


class ProfileDelete(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request):

        profile, created = Profile.objects.get_or_create(user=request.user)

        if profile.bio_pic:

            file_path = profile.bio_pic.path
            profile.bio_pic.delete(save=False)

            if os.path.exists(file_path):
                os.remove(file_path)

        return Response({"message": "Bio pic deleted"})


# # debug toolbar

# from django.test.utils import CaptureQueriesContext
# from django.db import connection
# from django.shortcuts import render
# from .models import Task

# def task_debug_view(request):

#     with CaptureQueriesContext(connection) as ctx_n1:
#         tasks_n1 = Task.objects.all()
#         for task in tasks_n1:
#             _ = task.created_by.username
#             if task.assigned_to:
#                 _ = task.assigned_to.username

#     with CaptureQueriesContext(connection) as ctx_fixed:
#         tasks_fixed = Task.objects.select_related("created_by", "assigned_to").all()
#         for task in tasks_fixed:
#             _ = task.created_by.username
#             if task.assigned_to:
#                 _ = task.assigned_to.username

#     return render(
#         request,
#         "debug_tasks.html",
#         {
#             "tasks": tasks_fixed,
#             "total_queries_fixed": len(ctx_fixed),
#             "total_queries_n1": len(ctx_n1),
#         },
#     )
