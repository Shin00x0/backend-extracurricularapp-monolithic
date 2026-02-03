import uuid
from django.db import models
from workers.models import Worker


class OperationStats(models.Model):
    """Daily operational statistics for workers."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='operation_stats')
    
    date = models.DateField(db_index=True)
    
    # Financial
    today_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pending_payments = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    weekly_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Activity
    active_services = models.IntegerField(default=0)
    total_completed_today = models.IntegerField(default=0)
    total_cancelled_today = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'stats'
        unique_together = ('worker', 'date')
        ordering = ['-date']
        indexes = [
            models.Index(fields=['worker', 'date']),
        ]
    
    def __str__(self):
        return f"Stats for {self.worker.code} on {self.date}"
