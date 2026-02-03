from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'message_type', 'is_read', 'timestamp']
    list_filter = ['message_type', 'is_read', 'timestamp']
    search_fields = ['sender__email', 'receiver__email', 'text']
    readonly_fields = ['id', 'timestamp']
    
    fieldsets = (
        ('Participants', {
            'fields': ('id', 'sender', 'receiver')
        }),
        ('Message', {
            'fields': ('text', 'message_type')
        }),
        ('Status', {
            'fields': ('is_read', 'timestamp')
        }),
    )
