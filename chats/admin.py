from django.contrib import admin
from .models import ChatRoom, Message


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'participant_1', 'participant_2', 'created_at', 'last_message_at']
    list_filter = ['created_at', 'last_message_at']
    search_fields = ['participant_1__email', 'participant_2__email']
    readonly_fields = ['id', 'created_at', 'room_name']
    
    fieldsets = (
        ('Room', {
            'fields': ('id', 'room_name')
        }),
        ('Participants', {
            'fields': ('participant_1', 'participant_2')
        }),
        ('Timeline', {
            'fields': ('created_at', 'last_message_at')
        }),
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'room', 'message_type', 'is_read', 'timestamp']
    list_filter = ['message_type', 'is_read', 'timestamp']
    search_fields = ['sender__email', 'text']
    readonly_fields = ['id', 'timestamp']
    
    fieldsets = (
        ('Message', {
            'fields': ('id', 'room', 'sender')
        }),
        ('Content', {
            'fields': ('text', 'message_type', 'attachment_url')
        }),
        ('Status', {
            'fields': ('is_read', 'timestamp')
        }),
    )
