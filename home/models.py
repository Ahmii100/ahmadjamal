from django.db import models
from django.utils import timezone
import uuid

class ContactMessage(models.Model):
    SERVICE_CHOICES = [
        ('android', 'Android App Development'),
        ('seo', 'SEO Optimization'),
        ('consulting', 'Digital Consulting'),
        ('other', 'Other / Not sure'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        ordering = ['-created_at']


class ServiceQuote(models.Model):
    """Store quotes from services page"""
    
    DELIVERY_CHOICES = [
        ('email', 'Email Only'),
        ('whatsapp', 'WhatsApp Only'),
        ('both', 'Both'),
    ]
    
    # Quote identification
    quote_id = models.CharField(max_length=50, unique=True, blank=True)
    
    # Customer information
    customer_name = models.CharField(max_length=100, blank=True)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20, blank=True)
    
    # Quote details (store as JSON)
    selected_services = models.JSONField()  # Stores list of selected items
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Delivery preferences
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_CHOICES, default='email')
    
    # Status
    is_read = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.quote_id:
            # Generate unique quote ID: Q-20240218-001
            today = timezone.now().strftime('%Y%m%d')
            last_quote = ServiceQuote.objects.filter(
                quote_id__startswith=f'Q-{today}'
            ).count()
            self.quote_id = f"Q-{today}-{str(last_quote + 1).zfill(3)}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.quote_id} - {self.customer_email}"