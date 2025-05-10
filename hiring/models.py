from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_recruiter = models.BooleanField(default=True)  # All users are recruiters by default

class ChatHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    sender = models.CharField(
        max_length=10,
        choices=[('user', 'User'), ('model', 'Model')],
        default='user'
    )
    timestamp = models.DateTimeField(auto_now_add=True)