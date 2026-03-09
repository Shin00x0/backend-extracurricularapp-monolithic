import uuid
from django.db import models
from django.utils import timezone


class BaseUser(models.Model):
    """Base user model linked to Firebase authentication."""
    
    ROLE_CHOICES = [
        ('user', 'Regular User'),
        ('client', 'Client'),
        ('worker', 'Worker'),
        ('admin', 'Administrator'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firebase_uid = models.CharField(max_length=128, unique=True, db_index=True, null=True, blank=True)
    email = models.EmailField(unique=True, db_index=True)
    name = models.CharField(max_length=255, blank=True)
    age = models.IntegerField(null=True, blank=True)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    # Location fields
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    # Profile
    images = models.JSONField(default=list, blank=True)  # Array of image URLs
    interests = models.JSONField(default=list, blank=True)  # Array of interest strings
    
    # Status
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    auth_provider = models.CharField(max_length=20, choices=[('firebase','Firebase'), ('local','Local')], default='firebase', db_index=True)
    last_login = models.DateTimeField(null=True, blank=True, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    password = models.CharField(max_length=128, blank=True)
    firebase_profile = models.JSONField(null=True, blank=True, default=dict)
    synced_at = models.DateTimeField(null=True, blank=True, db_index=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    
    class Meta:
        app_label = 'users'
        indexes = [
            models.Index(fields=['firebase_uid', 'email']),
            models.Index(fields=['role', 'is_online']),
            models.Index(fields=['auth_provider', 'is_active']),
            models.Index(fields=['last_login']),
            models.Index(fields=['synced_at']),
        ]
    
    def __str__(self):
        return f"{self.name,self.id,self.email} ({self.get_role_display()})"
    
    @property
    def is_client(self):
        return self.role == 'client'
    
    @property
    def is_worker(self):
        return self.role == 'worker'
    
    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_authenticated(self):
        """True when this object represents an authenticated user (for DRF perms)."""
        return True


class UserAvatar(models.Model):
    """Store uploaded avatars for users."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='avatar')
    url = models.URLField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'users'
    
    def __str__(self):
        return f"Avatar for {self.user.email}"


class DeviceToken(models.Model):
    """Store FCM tokens for push notifications."""
    
    PLATFORM_CHOICES = [
        ('android', 'Android'),
        ('ios', 'iOS'),
        ('web', 'Web'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='device_tokens')
    token = models.CharField(max_length=512, db_index=True)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        app_label = 'users'
        unique_together = ('user', 'token')
    
    def __str__(self):
        return f"{self.user.email} - {self.platform}"
