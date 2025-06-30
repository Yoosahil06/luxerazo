from django.contrib import admin
from .models import ConciergeRequest

@admin.register(ConciergeRequest)
class ConciergeRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'service_type', 'priority', 'status', 'created_at']
    list_filter = ['service_type', 'priority', 'status', 'created_at']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status', 'priority']
    
    fieldsets = (
        ('Client Information', {
            'fields': ('user', 'name', 'email', 'phone', 'preferred_contact')
        }),
        ('Service Details', {
            'fields': ('service_type', 'priority', 'subject', 'message', 'budget_range')
        }),
        ('Status & Tracking', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )
