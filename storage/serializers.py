"""Serializers for Storage models."""

from rest_framework import serializers
from storage.models import FileUpload


class FileUploadSerializer(serializers.ModelSerializer):
    """Serializer for FileUpload model."""
    
    class Meta:
        model = FileUpload
        fields = ['file_id', 'url', 'file_type', 'original_filename', 'file_size', 'mime_type', 'uploaded_at']
        read_only_fields = ['file_id', 'uploaded_at']


class FileUploadResponseSerializer(serializers.Serializer):
    """Serializer for file upload response."""
    
    file_id = serializers.CharField(max_length=50)
    url = serializers.URLField()
    uploaded_at = serializers.DateTimeField()
