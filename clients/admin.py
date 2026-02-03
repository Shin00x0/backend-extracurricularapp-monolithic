from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['code', 'user', 'client_type', 'total_spent', 'rating', 'verified_account', 'is_blocked']
    list_filter = ['client_type', 'verified_account', 'is_blocked', 'member_since']
    search_fields = ['code', 'user__email', 'user__name', 'company']
    readonly_fields = ['id', 'code', 'created_at', 'updated_at', 'member_since']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('id', 'user', 'code')
        }),
        ('Contact', {
            'fields': ('phone', 'company')
        }),
        ('Type & Status', {
            'fields': ('client_type', 'verified_account', 'is_blocked')
        }),
        ('Stats', {
            'fields': ('total_spent', 'total_requests', 'rating')
        }),
        ('Preferences', {
            'fields': ('favorite_workers', 'notes')
        }),
        ('Dates', {
            'fields': ('member_since', 'created_at', 'updated_at')
        }),
    )
