import uuid
from django.db import models
from users.models import BaseUser


def generate_worker_code():
    """Generate unique worker code like WK-0001."""
    from workers.models import Worker
    count = Worker.objects.count() + 1
    return f"WK-{count:04d}"


class Worker(models.Model):
    """Worker profile model."""
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('active', 'Active'),
        ('unavailable', 'Unavailable'),
        ('offline', 'Offline'),
    ]
    
    EMERGENCY_STATUS_CHOICES = [
        ('normal', 'Normal'),
        ('warning', 'Warning'),
        ('emergency', 'Emergency'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='worker_profile')
    code = models.CharField(max_length=20, unique=True, db_index=True, default=generate_worker_code)
    
    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='offline', db_index=True)
    is_online = models.BooleanField(default=False)
    last_update = models.DateTimeField(auto_now=True)
    
    # Current task
    current_request_id = models.UUIDField(null=True, blank=True)
    current_client_code = models.CharField(max_length=20, blank=True)
    current_location = models.CharField(max_length=255, blank=True)
    check_in_time = models.DateTimeField(null=True, blank=True)
    
    # Heartbeat/activity tracking
    heartbeat = models.BooleanField(default=False)
    
    # Emergency
    emergency_status = models.CharField(max_length=20, choices=EMERGENCY_STATUS_CHOICES, default='normal')
    
    # Stats
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    completed_services = models.IntegerField(default=0)
    total_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Professional info
    certifications = models.JSONField(default=list, blank=True)  # Array of certification strings
    verified_account = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'workers'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['user']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Worker {self.code} - {self.user.name or self.user.email}"
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_worker_code()
        super().save(*args, **kwargs)


class WorkerLocationPin(models.Model):
    """Real-time location tracking for workers."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='location_pins')
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        app_label = 'workers'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['worker', 'timestamp']),
        ]
    
    def __str__(self):
        return f"Location for {self.worker.code} at {self.timestamp}"
