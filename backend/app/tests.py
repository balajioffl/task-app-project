from django.test import TestCase
from django.contrib.auth.models import User,Group
from rest_framework.test import APITestCase
from rest_framework import status
from app.models import Task

# Create your tests here.

class TaskTest(APITestCase):

    def setUp(self):

        self.admin_group = Group.objects.create(name="Admin")
        self.manager_group = Group.objects.create(name="Manager")
        self.member_group = Group.objects.create(name="Member")

        self.admin_user = User.objects.create_user(username="admin", password="1234")
        self.manager_user = User.objects.create_user(username="manager", password="1234")
        self.member_user = User.objects.create_user(username="member", password="1234")

        self.admin_user.groups.add(self.admin_group)
        self.manager_user.groups.add(self.manager_group)
        self.member_user.groups.add(self.member_group)

        self.admin_task = Task.objects.create(
            title="Admin Task",
            description="Created by admin",
            status="pending",
            priority="medium",
            created_by=self.admin_user
        )

        self.manager_task = Task.objects.create(
            title="Manager Task",
            description="Created by manager",
            status="pending",
            priority="medium",
            created_by=self.manager_user
        )


    def test_member_can_view_tasks(self):

        self.client.force_authenticate(user=self.member_user)
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_admin_can_create_task(self):

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post("/api/tasks/", {
            "title": "New Task",
            "description": "Admin created",
            "status": "pending",
            "priority": "high"
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_manager_can_create_task(self):

        self.client.force_authenticate(user=self.manager_user)
        response = self.client.post("/api/tasks/", {
            "title": "New Task",
            "description": "Manager created",
            "status": "pending",
            "priority": "high"
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_member_cannot_create_task(self):

        self.client.force_authenticate(user=self.member_user)
        response = self.client.post("/api/tasks/", {
            "title": "Forbidden",
            "description": "Member create",
            "status": "pending",
            "priority": "low"
        })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_admin_can_update_any_task(self):

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(
            f"/api/tasks/{self.manager_task.id}/",
            {"status": "completed"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_manager_can_update_own_task(self):

        self.client.force_authenticate(user=self.manager_user)
        response = self.client.patch(
            f"/api/tasks/{self.manager_task.id}/",
            {"status": "completed"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_member_cannot_update_task(self):

        self.client.force_authenticate(user=self.member_user)
        response = self.client.patch(
            f"/api/tasks/{self.admin_task.id}/",
            {"status": "completed"}
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_admin_can_delete_task(self):

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f"/api/tasks/{self.admin_task.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_manager_cannot_delete_task(self):

        self.client.force_authenticate(user=self.manager_user)
        response = self.client.delete(f"/api/tasks/{self.manager_task.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_member_cannot_delete_task(self):

        self.client.force_authenticate(user=self.member_user)
        response = self.client.delete(f"/api/tasks/{self.admin_task.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
