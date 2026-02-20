from django.contrib import admin
from .models import ContactMessage, ServiceQuote

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'service', 'created_at', 'is_read')
    list_filter = ('service', 'is_read', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',)

@admin.register(ServiceQuote)
class ServiceQuoteAdmin(admin.ModelAdmin):
    list_display = ('quote_id', 'customer_email', 'total_amount', 'delivery_method', 'created_at', 'is_read')
    list_filter = ('delivery_method', 'is_read', 'created_at')
    search_fields = ('quote_id', 'customer_email', 'customer_name')
    readonly_fields = ('created_at',)