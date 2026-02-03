"""Serializers for WorkRequest models."""

from rest_framework import serializers
from work_requests.models import WorkRequest


class WorkRequestSerializer(serializers.ModelSerializer):
    """Serializer for WorkRequest model."""
    
    class Meta:
        model = WorkRequest
        fields = [
            'id', 'client_code', 'worker_code', 'service_type', 'location',
            'scheduled_at', 'payment', 'status', 'priority', 'notes',
            'images', 'confirmation_time', 'check_in_time', 'check_out_time',
            'rating', 'review', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'confirmation_time', 'check_in_time', 'check_out_time', 'created_at', 'updated_at'
        ]


class WorkRequestCreateSerializer(serializers.Serializer):
    """Serializer for creating a WorkRequest."""
    
    service_type = serializers.CharField(max_length=100)
    location = serializers.CharField(max_length=255)
    scheduled_at = serializers.DateTimeField()
    payment = serializers.DecimalField(max_digits=10, decimal_places=2)
    priority = serializers.ChoiceField(choices=['low', 'normal', 'high'], default='normal')
    notes = serializers.CharField(required=False, allow_blank=True)


class WorkRequestStatusUpdateSerializer(serializers.Serializer):
    """Serializer for updating work request status."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    status = serializers.ChoiceField(choices=STATUS_CHOICES)
    worker_code = serializers.CharField(max_length=20, required=False, allow_blank=True)


class WorkRequestRatingSerializer(serializers.Serializer):
    """Serializer for rating a completed work request."""
    
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, min_value=0, max_value=5)
    review = serializers.CharField(max_length=1000, required=False, allow_blank=True)


class WorkRequestCancelSerializer(serializers.Serializer):
    """Serializer for cancelling a work request."""
    
    reason = serializers.CharField(max_length=500, required=False, allow_blank=True)
