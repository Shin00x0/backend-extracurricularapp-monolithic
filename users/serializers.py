"""Serializers for User models."""

from rest_framework import serializers
from users.models import BaseUser, UserAvatar, DeviceToken


class UserAvatarSerializer(serializers.ModelSerializer):
    """Serializer for UserAvatar model."""
    
    class Meta:
        model = UserAvatar
        fields = ['url', 'uploaded_at']
        read_only_fields = ['uploaded_at']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for public user profile."""
    
    avatar = UserAvatarSerializer(read_only=True)
    
    class Meta:
        model = BaseUser
        fields = [
            'id', 'name', 'age', 'bio', 'phone', 'images', 'interests',
            'is_online', 'latitude', 'longitude', 'avatar', 'role'
        ]
        read_only_fields = ['id', 'role']


class BaseUserSerializer(serializers.ModelSerializer):
    """Serializer for BaseUser model."""
    
    avatar = UserAvatarSerializer(read_only=True)
    
    class Meta:
        model = BaseUser
        fields = [
            'id', 'firebase_uid', 'email', 'name', 'age', 'bio', 'phone',
            'latitude', 'longitude', 'images', 'interests', 'is_online',
            'last_seen', 'role', 'avatar', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'firebase_uid', 'email', 'role', 'created_at', 'updated_at']


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile."""
    
    class Meta:
        model = BaseUser
        fields = ['name', 'age', 'bio', 'phone', 'images', 'interests', 'latitude', 'longitude']


class UserVerifySerializer(serializers.Serializer):
    """Serializer for verified user response."""
    
    uid = serializers.CharField(source='firebase_uid')
    email = serializers.CharField()
    name = serializers.CharField(required=False, allow_blank=True)
    user_type = serializers.CharField(source='role')


class DeviceTokenSerializer(serializers.ModelSerializer):
    """Serializer for DeviceToken model."""
    
    class Meta:
        model = DeviceToken
        fields = ['id', 'token', 'platform', 'is_active', 'created_at', 'last_used']
        read_only_fields = ['id', 'created_at', 'last_used']


class DeviceTokenCreateSerializer(serializers.Serializer):
    """Serializer for creating a device token."""
    
    token = serializers.CharField(max_length=512)
    platform = serializers.ChoiceField(choices=['android', 'ios', 'web'])
class BaseUserSerializer(serializers.ModelSerializer):
    """Serializer for BaseUser model."""
    
    class Meta:
        model = BaseUser
        fields = [
            'id', 'firebase_uid', 'email', 'name', 'age', 'bio', 'phone',
            'latitude', 'longitude', 'images', 'interests', 'is_online',
            'last_seen', 'role', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'firebase_uid', 'created_at', 'updated_at']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile view (public)."""
    
    is_online = serializers.SerializerMethodField()
    
    class Meta:
        model = BaseUser
        fields = [
            'id', 'name', 'age', 'bio', 'images', 'interests',
            'is_online', 'role', 'latitude', 'longitude'
        ]
    
    def get_is_online(self, obj):
        return obj.is_online


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile."""
    
    class Meta:
        model = BaseUser
        fields = ['name', 'age', 'bio', 'phone', 'latitude', 'longitude', 'interests', 'images']


class UserAvatarSerializer(serializers.ModelSerializer):
    """Serializer for UserAvatar model."""
    
    class Meta:
        model = UserAvatar
        fields = ['id', 'url', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class DeviceTokenSerializer(serializers.ModelSerializer):
    """Serializer for DeviceToken model."""
    
    class Meta:
        model = DeviceToken
        fields = ['id', 'token', 'platform', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']
