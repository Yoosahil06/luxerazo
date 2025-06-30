from django.db import models
from django.contrib.auth.models import User

class ConciergeRequest(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Standard'),
        ('medium', 'Priority'),
        ('high', 'Urgent'),
        ('vip', 'VIP Client'),
    ]
    
    SERVICE_TYPES = [
        ('personal_shopping', 'Personal Shopping'),
        ('product_sourcing', 'Product Sourcing'),
        ('styling_consultation', 'Styling Consultation'),
        ('authentication', 'Authentication Service'),
        ('customization', 'Customization Request'),
        ('gift_service', 'Gift Service'),
        ('vip_appointment', 'VIP Appointment'),
        ('other', 'Other Request'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='low')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    budget_range = models.CharField(max_length=50, blank=True)
    preferred_contact = models.CharField(max_length=20, default='email')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Concierge Request'
        verbose_name_plural = 'Concierge Requests'
    
    def __str__(self):
        return f"{self.name} - {self.service_type} ({self.status})"
