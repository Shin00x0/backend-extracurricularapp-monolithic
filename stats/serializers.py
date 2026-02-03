"""Serializers for Stats models."""

from rest_framework import serializers
from stats.models import OperationStats


class OperationStatsSerializer(serializers.ModelSerializer):
    """Serializer for OperationStats model."""
    
    class Meta:
        model = OperationStats
        fields = [
            'id', 'worker', 'date', 'today_earnings', 'active_services',
            'pending_payments', 'weekly_earnings', 'total_completed_today',
            'total_cancelled_today', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for dashboard statistics."""
    
    today_earnings = serializers.DecimalField(max_digits=10, decimal_places=2)
    active_services = serializers.IntegerField()
    pending_payments = serializers.DecimalField(max_digits=10, decimal_places=2)
    weekly_earnings = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_completed_today = serializers.IntegerField()
    total_cancelled_today = serializers.IntegerField()
