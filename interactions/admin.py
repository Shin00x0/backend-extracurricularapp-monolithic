from django.contrib import admin
from .models import UserInteraction, Match


@admin.register(UserInteraction)
class UserInteractionAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'interaction_type', 'is_matched', 'timestamp']
    list_filter = ['interaction_type', 'is_matched', 'timestamp']
    search_fields = ['from_user__email', 'to_user__email']
    readonly_fields = ['id', 'timestamp']
    
    fieldsets = (
        ('Interaction', {
            'fields': ('id', 'from_user', 'to_user', 'interaction_type')
        }),
        ('Match Status', {
            'fields': ('is_matched', 'timestamp')
        }),
    )


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['user_1', 'user_2', 'matched_at', 'is_active']
    list_filter = ['is_active', 'matched_at']
    search_fields = ['user_1__email', 'user_2__email']
    readonly_fields = ['id', 'matched_at']
    
    fieldsets = (
        ('Match', {
            'fields': ('id', 'user_1', 'user_2')
        }),
        ('Conversation', {
            'fields': ('conversation_started_at', 'is_active')
        }),
        ('Timeline', {
            'fields': ('matched_at',)
        }),
    )
