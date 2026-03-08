from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    role_choices = (
        ('MANAGER', 'Manager'),
        ('MEMBER', 'Member')
    )
    role = models.CharField(max_length=20, choices=role_choices, default='MEMBER')
    is_deleted = models.BooleanField(default=False)




class Task(models.Model):
    status_choices = (
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
    )
    Priority_choices = (
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
    )
    title = models.CharField(max_length=100)
    description = models.TextField
    status = models.CharField(max_length=20, choices=status_choices, default='Pending')
    priority = models.CharField(max_length=20, choices=Priority_choices, )
    due_date = models.DateTimeField()

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_created')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_assigned')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
