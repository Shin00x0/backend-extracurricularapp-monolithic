import uuid
from django.db import models
from django.utils import timezone
from users.models import BaseUser


def generate_client_code():
    """Generate unique client code like CL-0001."""
    from clients.models import Client
    count = Client.objects.count() + 1
    return f"CL-{count:04d}"


class Client(models.Model):
    """Client profile model."""
    
    CLIENT_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('vip', 'VIP'),
        ('corporate', 'Corporate'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='client_profile')
    code = models.CharField(max_length=20, unique=True, db_index=True, default=generate_client_code)
    
    phone = models.CharField(max_length=20, blank=True)
    client_type = models.CharField(max_length=20, choices=CLIENT_TYPE_CHOICES, default='individual')
    company = models.CharField(max_length=255, blank=True, null=True)
    
    # Stats
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_requests = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    
    # Account status
    verified_account = models.BooleanField(default=False)
    member_since = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    is_blocked = models.BooleanField(default=False)
    
    # Preferences
    favorite_workers = models.JSONField(default=list, blank=True)  # List of worker codes
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'clients'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        return f"Client {self.code} - {self.user.email}"
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_client_code()
        super().save(*args, **kwargs)
