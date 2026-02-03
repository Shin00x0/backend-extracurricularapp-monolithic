import uuid
from django.db import models
from users.models import BaseUser


class FileUpload(models.Model):
    """File upload tracking model."""
    
    FILE_TYPE_CHOICES = [
        ('image', 'Image'),
        ('document', 'Document'),
        ('avatar', 'Avatar'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='uploads', null=True, blank=True)
    
    file_id = models.CharField(max_length=50, unique=True, db_index=True)
    url = models.URLField()
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES, default='image')
    original_filename = models.CharField(max_length=255, blank=True)
    file_size = models.BigIntegerField(null=True, blank=True)  # in bytes
    mime_type = models.CharField(max_length=128, blank=True)
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'storage'
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['user', 'uploaded_at']),
            models.Index(fields=['file_type']),
        ]
    
    def __str__(self):
        return f"File {self.file_id} - {self.original_filename}"
