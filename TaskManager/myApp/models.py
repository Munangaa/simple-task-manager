from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CASCADE


# Create your models here.
class Metadata(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class States(Metadata):
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('DISABLED', 'Disabled'),
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('DELETED', 'Deleted'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
    )
    status_type = models.CharField(choices=STATUS_CHOICES, default='ACTIVE', max_length=20)
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=100, null=True)


class Role(Metadata):
    name = models.CharField(max_length=20)
    state = models.ForeignKey(States, on_delete=CASCADE, null=True)


class Permission(Metadata):
    name = models.CharField(max_length=20,)
    codename = models.CharField(max_length=30)
    description = models.TextField(max_length=100, null=True)


class RolePermission(Metadata):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)


class User(AbstractUser, Metadata):

    user_role = models.ForeignKey(Role, on_delete=CASCADE , default=1)


class Task(Metadata):
    Priority_choices = (
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
    )
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=100, null=True)

    priority = models.CharField(max_length=20, choices=Priority_choices, )
    due_date = models.DateTimeField(null=True)
    status = models.ForeignKey(States, on_delete=CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_created',null=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_assigned', null=True)
