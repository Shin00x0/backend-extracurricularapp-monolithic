from django.contrib import admin
from .models import FileUpload


@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    list_display = ['file_id', 'original_filename', 'file_type', 'user', 'uploaded_at']
    list_filter = ['file_type', 'uploaded_at']
    search_fields = ['file_id', 'original_filename', 'user__email']
    readonly_fields = ['id', 'file_id', 'uploaded_at']
    
    fieldsets = (
        ('File Info', {
            'fields': ('id', 'file_id', 'original_filename')
        }),
        ('Details', {
            'fields': ('file_type', 'mime_type', 'file_size')
        }),
        ('URL', {
            'fields': ('url',)
        }),
        ('User', {
            'fields': ('user',)
        }),
        ('Uploaded', {
            'fields': ('uploaded_at',)
        }),
    )
