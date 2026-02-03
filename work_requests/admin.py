from django.contrib import admin
from .models import WorkRequest


@admin.register(WorkRequest)
class WorkRequestAdmin(admin.ModelAdmin):
    list_display = ['client_code', 'service_type', 'status', 'scheduled_at', 'payment', 'rating']
    list_filter = ['status', 'priority', 'scheduled_at', 'created_at']
    search_fields = ['client_code', 'worker_code', 'service_type', 'location']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Request ID', {
            'fields': ('id',)
        }),
        ('Participants', {
            'fields': ('client_code', 'worker_code')
        }),
        ('Service Details', {
            'fields': ('service_type', 'location', 'scheduled_at', 'payment')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority')
        }),
        ('Timeline', {
            'fields': ('confirmation_time', 'check_in_time', 'check_out_time')
        }),
        ('Feedback', {
            'fields': ('rating', 'review')
        }),
        ('Additional Info', {
            'fields': ('notes', 'images')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
