from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.name

    
class Task(models.Model):

    STATUS_CHOICES = [
        ('pending','Pending'),
        ('in_progress','In Progress'),
        ('completed','Completed'),
    ]

    PRIORIY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    priority = models.CharField(max_length=10,choices=PRIORIY_CHOICES,default='low')
    due_date = models.DateField(null=True,blank=True)

    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='created_task')
    assigned_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='assigned_tasks')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
