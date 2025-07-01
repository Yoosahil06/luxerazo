from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from .models import Cart, CartItem, Wishlist, Order, OrderItem, ShippingLabel, OrderNote, CustomerCommunication
import csv

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_items', 'subtotal', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email')
    inlines = [CartItemInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('total_price',)

class ShippingLabelInline(admin.TabularInline):
    model = ShippingLabel
    extra = 0
    readonly_fields = ('created_at',)

class OrderNoteInline(admin.TabularInline):
    model = OrderNote
    extra = 1
    fields = ('note_type', 'content', 'created_by')

class CustomerCommunicationInline(admin.TabularInline):
    model = CustomerCommunication
    extra = 0
    readonly_fields = ('sent_at', 'delivered_at', 'created_at')

def generate_shipping_label(modeladmin, request, queryset):
    """Generate shipping labels for selected orders"""
    for order in queryset:
        if order.status in ['confirmed', 'processing', 'packed']:
            # This would integrate with actual shipping API
            ShippingLabel.objects.create(
                order=order,
                carrier='dhl',
                tracking_number=f'DHL{order.id:08d}',
                label_url=f'https://example.com/labels/{order.id}.pdf'
            )
    modeladmin.message_user(request, f"Shipping labels generated for {queryset.count()} orders.")
generate_shipping_label.short_description = "Generate shipping labels"

def mark_as_shipped(modeladmin, request, queryset):
    """Mark selected orders as shipped"""
    from django.utils import timezone
    queryset.update(status='shipped', shipped_at=timezone.now())
    modeladmin.message_user(request, f"{queryset.count()} orders marked as shipped.")
mark_as_shipped.short_description = "Mark as shipped"

def send_order_confirmation(modeladmin, request, queryset):
    """Send order confirmation emails"""
    for order in queryset:
        CustomerCommunication.objects.create(
            order=order,
            comm_type='email',
            subject=f'Order Confirmation - {order.order_number}',
            content=f'Your order {order.order_number} has been confirmed.',
            recipient=order.shipping_email,
            status='pending'
        )
    modeladmin.message_user(request, f"Confirmation emails queued for {queryset.count()} orders.")
send_order_confirmation.short_description = "Send order confirmations"

def export_orders_csv(modeladmin, request, queryset):
    """Export selected orders to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Order Number', 'Customer', 'Status', 'Total', 'Payment Status', 'Created At'])
    
    for order in queryset:
        writer.writerow([
            order.order_number,
            order.user.username,
            order.status,
            order.total,
            order.payment_status,
            order.created_at.strftime('%Y-%m-%d %H:%M')
        ])
    
    return response
export_orders_csv.short_description = "Export selected orders to CSV"

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status_badge', 'payment_status_badge', 'total', 'shipping_status', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at', 'shipping_country')
    search_fields = ('order_number', 'user__username', 'user__email', 'shipping_email', 'shipping_name')
    readonly_fields = ('order_number', 'created_at', 'updated_at', 'confirmed_at', 'processed_at', 'shipped_at', 'delivered_at')
    inlines = [OrderItemInline, ShippingLabelInline, OrderNoteInline, CustomerCommunicationInline]
    actions = [generate_shipping_label, mark_as_shipped, send_order_confirmation, export_orders_csv]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'created_at', 'updated_at')
        }),
        ('Shipping Details', {
            'fields': ('shipping_name', 'shipping_email', 'shipping_phone', 'shipping_address', 
                      'shipping_city', 'shipping_country', 'shipping_postal_code', 'shipping_instructions')
        }),
        ('Order Totals', {
            'fields': ('subtotal', 'shipping_cost', 'tax_amount', 'total', 'total_amount')
        }),
        ('Payment', {
            'fields': ('payment_method', 'payment_status', 'stripe_payment_intent_id')
        }),
        ('Return/Refund', {
            'fields': ('return_requested_at', 'return_reason', 'refund_amount', 'refund_status', 'refund_processed_at'),
            'classes': ('collapse',)
        }),
        ('Timeline', {
            'fields': ('confirmed_at', 'processed_at', 'shipped_at', 'delivered_at'),
            'classes': ('collapse',)
        })
    )

    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'confirmed': 'blue',
            'processing': 'purple',
            'packed': 'teal',
            'shipped': 'green',
            'delivered': 'darkgreen',
            'cancelled': 'red',
            'returned': 'gray'
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def payment_status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'authorized': 'blue',
            'paid': 'green',
            'failed': 'red',
            'refunded': 'gray'
        }
        color = colors.get(obj.payment_status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_payment_status_display()
        )
    payment_status_badge.short_description = 'Payment'

    def shipping_status(self, obj):
        labels = obj.shipping_labels.all()
        if labels:
            label = labels.first()
            return format_html(
                '<a href="{}" target="_blank">{} - {}</a>',
                label.label_url,
                label.carrier.upper(),
                label.tracking_number
            )
        return "No shipping label"
    shipping_status.short_description = 'Shipping'

class ShippingLabelAdmin(admin.ModelAdmin):
    list_display = ('order', 'carrier', 'tracking_number', 'created_at', 'printed_at')
    list_filter = ('carrier', 'created_at')
    search_fields = ('order__order_number', 'tracking_number')
    readonly_fields = ('created_at',)

class OrderNoteAdmin(admin.ModelAdmin):
    list_display = ('order', 'note_type', 'content_preview', 'created_by', 'created_at')
    list_filter = ('note_type', 'created_at')
    search_fields = ('order__order_number', 'content')
    readonly_fields = ('created_at',)

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'

class CustomerCommunicationAdmin(admin.ModelAdmin):
    list_display = ('order', 'comm_type', 'subject', 'recipient', 'status', 'sent_at')
    list_filter = ('comm_type', 'status', 'created_at')
    search_fields = ('order__order_number', 'subject', 'recipient')
    readonly_fields = ('sent_at', 'delivered_at', 'created_at')

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'product__name')

admin.site.register(Cart, CartAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ShippingLabel, ShippingLabelAdmin)
admin.site.register(OrderNote, OrderNoteAdmin)
admin.site.register(CustomerCommunication, CustomerCommunicationAdmin)
