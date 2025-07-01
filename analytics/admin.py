from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, Avg, Count
from django.urls import path
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import (
    SalesReport, ProductAnalytics, CustomerInsight, 
    TrafficSource, ConversionFunnel, TopSellingProduct
)

class SalesReportAdmin(admin.ModelAdmin):
    list_display = ('period', 'start_date', 'end_date', 'total_orders', 'total_revenue', 'average_order_value', 'new_customers')
    list_filter = ('period', 'start_date')
    readonly_fields = ('created_at',)
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_site.admin_view(self.dashboard_view), name='analytics_dashboard'),
        ]
        return custom_urls + urls
    
    def dashboard_view(self, request):
        # Get recent sales data
        recent_reports = SalesReport.objects.filter(period='daily').order_by('-start_date')[:30]
        
        # Calculate key metrics
        total_revenue = SalesReport.objects.aggregate(Sum('total_revenue'))['total_revenue__sum'] or 0
        total_orders = SalesReport.objects.aggregate(Sum('total_orders'))['total_orders__sum'] or 0
        avg_order_value = SalesReport.objects.aggregate(Avg('average_order_value'))['average_order_value__avg'] or 0
        
        context = {
            'title': 'Analytics Dashboard',
            'recent_reports': recent_reports,
            'total_revenue': total_revenue,
            'total_orders': total_orders,
            'avg_order_value': avg_order_value,
        }
        return render(request, 'admin/analytics/dashboard.html', context)

class ProductAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('product', 'date', 'views', 'add_to_cart', 'purchases', 'revenue', 'conversion_rate_display')
    list_filter = ('date', 'product__category', 'product__brand')
    search_fields = ('product__name',)
    readonly_fields = ('conversion_rate',)
    
    def conversion_rate_display(self, obj):
        return format_html(
            '<span style="color: {};">{:.2f}%</span>',
            'green' if obj.conversion_rate >= 2.0 else 'orange' if obj.conversion_rate >= 1.0 else 'red',
            obj.conversion_rate
        )
    conversion_rate_display.short_description = 'Conversion Rate'

class CustomerInsightAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_orders', 'total_spent', 'average_order_value', 'customer_segment', 'last_purchase_date')
    list_filter = ('first_purchase_date', 'last_purchase_date')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('last_updated',)
    actions = ['update_insights']
    
    def customer_segment(self, obj):
        if obj.total_spent >= 10000:
            return format_html('<span style="color: gold; font-weight: bold;">VIP</span>')
        elif obj.total_spent >= 5000:
            return format_html('<span style="color: purple; font-weight: bold;">Premium</span>')
        elif obj.total_spent >= 1000:
            return format_html('<span style="color: blue; font-weight: bold;">Regular</span>')
        else:
            return format_html('<span style="color: gray;">New</span>')
    customer_segment.short_description = 'Segment'
    
    def update_insights(self, request, queryset):
        for insight in queryset:
            insight.update_insights()
        self.message_user(request, f"Updated insights for {queryset.count()} customers.")
    update_insights.short_description = "Update customer insights"

class TrafficSourceAdmin(admin.ModelAdmin):
    list_display = ('source', 'date', 'visitors', 'sessions', 'bounce_rate_display', 'conversion_rate_display', 'revenue')
    list_filter = ('source', 'date')
    
    def bounce_rate_display(self, obj):
        return format_html(
            '<span style="color: {};">{:.1f}%</span>',
            'red' if obj.bounce_rate >= 70 else 'orange' if obj.bounce_rate >= 50 else 'green',
            obj.bounce_rate
        )
    bounce_rate_display.short_description = 'Bounce Rate'
    
    def conversion_rate_display(self, obj):
        return format_html(
            '<span style="color: {};">{:.2f}%</span>',
            'green' if obj.conversion_rate >= 2.0 else 'orange' if obj.conversion_rate >= 1.0 else 'red',
            obj.conversion_rate
        )
    conversion_rate_display.short_description = 'Conversion Rate'

class ConversionFunnelAdmin(admin.ModelAdmin):
    list_display = ('date', 'visitors', 'product_views', 'add_to_cart', 'checkout_started', 'orders_completed', 'overall_conversion_display')
    list_filter = ('date',)
    readonly_fields = ('product_view_rate', 'add_to_cart_rate', 'checkout_rate', 'completion_rate', 'overall_conversion_rate')
    
    def overall_conversion_display(self, obj):
        return format_html(
            '<span style="color: {}; font-weight: bold;">{:.2f}%</span>',
            'green' if obj.overall_conversion_rate >= 3.0 else 'orange' if obj.overall_conversion_rate >= 1.5 else 'red',
            obj.overall_conversion_rate
        )
    overall_conversion_display.short_description = 'Overall Conversion'

class TopSellingProductAdmin(admin.ModelAdmin):
    list_display = ('rank', 'product', 'period_range', 'units_sold', 'revenue')
    list_filter = ('period_start', 'period_end')
    search_fields = ('product__name',)
    ordering = ('rank',)
    
    def period_range(self, obj):
        return f"{obj.period_start} to {obj.period_end}"
    period_range.short_description = 'Period'

# Custom admin site configuration
class AnalyticsAdminSite(admin.AdminSite):
    site_header = 'Luxerazo Analytics Dashboard'
    site_title = 'Analytics'
    index_title = 'Analytics Dashboard'

# Register models
admin.site.register(SalesReport, SalesReportAdmin)
admin.site.register(ProductAnalytics, ProductAnalyticsAdmin)
admin.site.register(CustomerInsight, CustomerInsightAdmin)
admin.site.register(TrafficSource, TrafficSourceAdmin)
admin.site.register(ConversionFunnel, ConversionFunnelAdmin)
admin.site.register(TopSellingProduct, TopSellingProductAdmin)
