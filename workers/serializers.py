"""Serializers for Worker models."""

from rest_framework import serializers
from workers.models import Worker, WorkerLocationPin
from users.serializers import BaseUserSerializer


class WorkerLocationPinSerializer(serializers.ModelSerializer):
    """Serializer for WorkerLocationPin model."""
    
    class Meta:
        model = WorkerLocationPin
        fields = ['id', 'latitude', 'longitude', 'timestamp']
        read_only_fields = ['id', 'timestamp']


class WorkerSerializer(serializers.ModelSerializer):
    """Serializer for Worker model."""
    
    user = BaseUserSerializer(read_only=True)
    
    class Meta:
        model = Worker
        fields = [
            'id', 'user', 'code', 'status', 'is_online', 'last_update',
            'current_request_id', 'current_client_code', 'current_location',
            'check_in_time', 'emergency_status', 'rating', 'completed_services',
            'total_earnings', 'certifications', 'verified_account', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'code', 'last_update', 'completed_services', 'total_earnings', 'created_at', 'updated_at'
        ]


class WorkerCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a Worker."""
    
    class Meta:
        model = Worker
        fields = ['certifications']


class WorkerStatusUpdateSerializer(serializers.Serializer):
    """Serializer for updating worker status."""
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('active', 'Active'),
        ('unavailable', 'Unavailable'),
        ('offline', 'Offline'),
    ]
    
    status = serializers.ChoiceField(choices=STATUS_CHOICES)


class WorkerLocationUpdateSerializer(serializers.Serializer):
    """Serializer for updating worker location."""
    
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()


class WorkerEmergencyStatusSerializer(serializers.Serializer):
    """Serializer for updating emergency status."""
    
    EMERGENCY_CHOICES = [
        ('normal', 'Normal'),
        ('warning', 'Warning'),
        ('emergency', 'Emergency'),
    ]
    
    emergency_status = serializers.ChoiceField(choices=EMERGENCY_CHOICES)


class WorkerNearbySerializer(serializers.Serializer):
    """Serializer for nearby workers query."""
    
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    radius = serializers.FloatField(default=5.0)  # km
