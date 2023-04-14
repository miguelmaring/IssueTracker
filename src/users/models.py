from django.db import models
from django.contrib.auth.models import AbstractUser

from issues.models import Issue

# Create your models here.
class Log(models.Model):
    CREATE = 'create'
    DELETE = 'delete'
    EDIT = 'edit'
    CHANGE_TYPES = [
        (CREATE, 'Create'),
        (DELETE, 'Delete'),
        (EDIT, 'Edit'),
    ]

    issue = models.ForeignKey(Issue, on_delete=models.SET_NULL, null=True, blank=False)
    issue_name = models.CharField(max_length=60, blank=False)
    change_type = models.CharField(max_length=6, choices=CHANGE_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    issue_deadline =  models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

class User(AbstractUser):
    """Add more fields to default user model."""

    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    issues_watched = models.ManyToManyField(Issue, blank=True)
    bio = models.CharField(max_length=280, blank=True, null=True)
    logs = models.ManyToManyField(Log, blank=True)