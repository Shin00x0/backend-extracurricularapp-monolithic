import uuid
from django.db import models
from users.models import BaseUser


class Message(models.Model):
    """Chat message model."""
    
    MESSAGE_TYPE_CHOICES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('location', 'Location'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='received_messages')
    
    text = models.TextField()
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, default='text')
    is_read = models.BooleanField(default=False, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        app_label = 'messaging'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['sender', 'receiver', 'timestamp']),
            models.Index(fields=['receiver', 'is_read']),
        ]
    
    def __str__(self):
        return f"Message from {self.sender.email} to {self.receiver.email}"
    
    def mark_as_read(self):
        """Mark message as read."""
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])
