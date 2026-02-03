from django.contrib import admin
from .models import Worker, WorkerLocationPin


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ['code', 'user', 'status', 'is_online', 'rating', 'completed_services', 'verified_account']
    list_filter = ['status', 'is_online', 'verified_account', 'emergency_status', 'created_at']
    search_fields = ['code', 'user__email', 'user__name']
    readonly_fields = ['id', 'code', 'created_at', 'updated_at', 'last_update']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('id', 'user', 'code')
        }),
        ('Status', {
            'fields': ('status', 'is_online', 'emergency_status', 'last_update')
        }),
        ('Current Task', {
            'fields': ('current_request_id', 'current_client_code', 'current_location', 'check_in_time', 'heartbeat')
        }),
        ('Professional', {
            'fields': ('verified_account', 'certifications')
        }),
        ('Stats', {
            'fields': ('rating', 'completed_services', 'total_earnings')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(WorkerLocationPin)
class WorkerLocationPinAdmin(admin.ModelAdmin):
    list_display = ['worker', 'latitude', 'longitude', 'timestamp']
    list_filter = ['timestamp', 'worker']
    search_fields = ['worker__code', 'worker__user__email']
    readonly_fields = ['id', 'timestamp']
    
    fieldsets = (
        ('Location', {
            'fields': ('id', 'worker', 'latitude', 'longitude')
        }),
        ('Timestamp', {
            'fields': ('timestamp',)
        }),
    )
