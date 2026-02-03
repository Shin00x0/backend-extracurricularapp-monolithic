import uuid
from django.db import models
from django.utils import timezone


class WorkRequest(models.Model):
    """Work request/service request model."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Client and Worker info
    client_code = models.CharField(max_length=20, db_index=True)  # Reference to Client.code
    worker_code = models.CharField(max_length=20, null=True, blank=True, db_index=True)  # Reference to Worker.code
    
    # Service details
    service_type = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    scheduled_at = models.DateTimeField()
    payment = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    
    # Additional info
    notes = models.TextField(blank=True)
    images = models.JSONField(default=list, blank=True)  # Service images
    
    # Timestamps
    confirmation_time = models.DateTimeField(null=True, blank=True)
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    
    # Ratings and reviews
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    review = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'work_requests'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['client_code', 'status']),
            models.Index(fields=['worker_code', 'status']),
            models.Index(fields=['status', 'scheduled_at']),
        ]
    
    def __str__(self):
        return f"WorkRequest {self.id} - {self.service_type} ({self.status})"
    
    @property
    def is_active(self):
        return self.status == 'active'
    
    @property
    def is_completed(self):
        return self.status == 'completed'
    
    @property
    def can_be_rated(self):
        return self.status == 'completed' and self.rating is None
