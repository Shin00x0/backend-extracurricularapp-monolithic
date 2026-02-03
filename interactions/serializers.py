"""Serializers for Interaction models."""

from rest_framework import serializers
from interactions.models import UserInteraction, Match
from users.serializers import UserProfileSerializer


class UserInteractionSerializer(serializers.ModelSerializer):
    """Serializer for UserInteraction model."""
    
    class Meta:
        model = UserInteraction
        fields = ['id', 'from_user', 'to_user', 'interaction_type', 'is_matched', 'timestamp']
        read_only_fields = ['id', 'is_matched', 'timestamp']


class UserInteractionCreateSerializer(serializers.Serializer):
    """Serializer for creating an interaction."""
    
    to_user_id = serializers.CharField(max_length=36)
    interaction_type = serializers.ChoiceField(choices=['like', 'pass'])


class MatchSerializer(serializers.ModelSerializer):
    """Serializer for Match model."""
    
    user_1_profile = serializers.SerializerMethodField()
    user_2_profile = serializers.SerializerMethodField()
    
    class Meta:
        model = Match
        fields = [
            'id', 'user_1', 'user_2', 'user_1_profile', 'user_2_profile',
            'matched_at', 'conversation_started_at', 'is_active'
        ]
        read_only_fields = ['id', 'matched_at', 'conversation_started_at']
    
    def get_user_1_profile(self, obj):
        return UserProfileSerializer(obj.user_1).data
    
    def get_user_2_profile(self, obj):
        return UserProfileSerializer(obj.user_2).data
