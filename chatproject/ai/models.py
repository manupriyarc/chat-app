# ai/models.py

from django.db import models
from accounts.models import CustomUser

class AIChat(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AIChatMessage(models.Model):
    chat = models.ForeignKey(AIChat, on_delete=models.CASCADE, related_name='messages')
    message = models.TextField()
    is_user = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']