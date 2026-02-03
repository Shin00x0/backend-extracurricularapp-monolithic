"""Serializers for Client models."""

from rest_framework import serializers
from clients.models import Client
from users.serializers import BaseUserSerializer


class ClientSerializer(serializers.ModelSerializer):
    """Serializer for Client model."""
    
    user = BaseUserSerializer(read_only=True)
    
    class Meta:
        model = Client
        fields = [
            'id', 'user', 'code', 'phone', 'client_type', 'company',
            'total_spent', 'total_requests', 'rating', 'verified_account',
            'member_since', 'favorite_workers', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'code', 'total_spent', 'total_requests', 'member_since', 'created_at', 'updated_at']


class ClientCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a Client."""
    
    class Meta:
        model = Client
        fields = ['phone', 'client_type', 'company']


class ClientUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating a Client."""
    
    class Meta:
        model = Client
        fields = ['phone', 'client_type', 'company', 'favorite_workers']
