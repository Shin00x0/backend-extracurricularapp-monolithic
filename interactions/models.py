import uuid
from django.db import models
from users.models import BaseUser


class UserInteraction(models.Model):
    """Like or pass interaction between users."""
    
    INTERACTION_TYPE_CHOICES = [
        ('like', 'Like'),
        ('pass', 'Pass'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='interactions_from')
    to_user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='interactions_to')
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPE_CHOICES)
    is_matched = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'interactions'
        unique_together = ('from_user', 'to_user')
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['from_user', 'interaction_type']),
            models.Index(fields=['to_user', 'interaction_type']),
        ]
    
    def __str__(self):
        return f"{self.from_user.email} {self.interaction_type} {self.to_user.email}"


class Match(models.Model):
    """Mutual match between two users."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_1 = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='matches_as_user1')
    user_2 = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='matches_as_user2')
    matched_at = models.DateTimeField(auto_now_add=True)
    conversation_started_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        app_label = 'interactions'
        unique_together = ('user_1', 'user_2')
        ordering = ['-matched_at']
        indexes = [
            models.Index(fields=['user_1', 'is_active']),
            models.Index(fields=['user_2', 'is_active']),
        ]
    
    def __str__(self):
        return f"Match: {self.user_1.email} ↔ {self.user_2.email}"

