from django.contrib import admin
from .models import OperationStats


@admin.register(OperationStats)
class OperationStatsAdmin(admin.ModelAdmin):
    list_display = ['worker', 'date', 'today_earnings', 'total_completed_today', 'active_services']
    list_filter = ['date', 'worker']
    search_fields = ['worker__code', 'worker__user__email']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Worker & Date', {
            'fields': ('id', 'worker', 'date')
        }),
        ('Financial', {
            'fields': ('today_earnings', 'pending_payments', 'weekly_earnings')
        }),
        ('Activity', {
            'fields': ('active_services', 'total_completed_today', 'total_cancelled_today')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
