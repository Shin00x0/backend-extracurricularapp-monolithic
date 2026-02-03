import uuid
from django.db import models
from django.utils import timezone
from users.models import BaseUser


class ChatRoom(models.Model):
    """Chat room for direct messaging between two users."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participant_1 = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='chat_rooms_as_p1')
    participant_2 = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='chat_rooms_as_p2')
    
    created_at = models.DateTimeField(auto_now_add=True)
    last_message_at = models.DateTimeField(null=True, blank=True, db_index=True)
    
    class Meta:
        app_label = 'chats'
        unique_together = ('participant_1', 'participant_2')
        ordering = ['-last_message_at']
        indexes = [
            models.Index(fields=['participant_1', 'last_message_at']),
            models.Index(fields=['participant_2', 'last_message_at']),
        ]
    
    def __str__(self):
        return f"ChatRoom: {self.participant_1.email} ↔ {self.participant_2.email}"
    
    @property
    def room_name(self):
        """Generate WebSocket room name for this chat."""
        # Sort UUIDs to ensure consistent room names
        ids = sorted([str(self.participant_1.id), str(self.participant_2.id)])
        return f"chat_{ids[0]}_{ids[1]}"


class Message(models.Model):
    """Chat message model."""
    
    MESSAGE_TYPE_CHOICES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('location', 'Location'),
        ('file', 'File'),
        ('audio', 'Audio'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='sent_messages')
    
    # Content
    text = models.TextField(blank=True, null=True)  # For text messages
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, default='text')
    
    # Attachments
    attachment_url = models.URLField(null=True, blank=True)  # For image, file, etc.
    audio_file = models.FileField(
        upload_to='voice_messages/%Y/%m/%d/',
        null=True,
        blank=True,
        help_text='Audio file for voice messages (max 5MB)'
    )
    audio_duration = models.FloatField(null=True, blank=True, help_text='Duration in seconds')
    
    # Status
    is_read = models.BooleanField(default=False, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        app_label = 'chats'
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['room', 'timestamp']),
            models.Index(fields=['sender', 'is_read']),
            models.Index(fields=['room', 'is_read']),
        ]
    
    def __str__(self):
        return f"Message from {self.sender.email} in {self.room.id}"
    
    def mark_as_read(self):
        """Mark message as read."""
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])
    
    def get_audio_url(self):
        """Get the audio file URL."""
        if self.audio_file:
            return self.audio_file.url
        return None
