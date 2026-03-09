"""Admin configuration for users app."""

from django.contrib import admin
from .models import BaseUser, UserAvatar, DeviceToken


@admin.register(BaseUser)
class BaseUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'role', 'is_online', 'is_active', 'is_staff', 'created_at']
    list_filter = ['role', 'is_online', 'is_active', 'created_at']
    search_fields = ['email', 'name', 'firebase_uid']
    readonly_fields = ['id', 'firebase_uid', 'created_at', 'updated_at', 'last_login']
    
    fieldsets = (
        ('Authentication', {
            'fields': ('id', 'firebase_uid', 'email', 'password', 'auth_provider')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
        ('Personal Info', {
            'fields': ('name', 'age', 'bio', 'phone')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude')
        }),
        ('Profile', {
            'fields': ('images', 'interests')
        }),
        ('Status', {
            'fields': ('is_online', 'last_seen', 'role', 'last_login')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def save_model(self, request, obj, form, change):
        """Hash plaintext password when set via admin interface."""
        from django.contrib.auth.hashers import make_password
        if obj.password and not obj.password.startswith('pbkdf2_'):
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)


@admin.register(UserAvatar)
class UserAvatarAdmin(admin.ModelAdmin):
    list_display = ['user', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['user__email']
    readonly_fields = ['id', 'uploaded_at']


@admin.register(DeviceToken)
class DeviceTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'platform', 'is_active', 'created_at']
    list_filter = ['platform', 'is_active', 'created_at']
    search_fields = ['user__email', 'token']
    readonly_fields = ['id', 'created_at', 'last_used']
