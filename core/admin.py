from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from django.db.models import Sum, Count
from products.models import Product, Brand
from orders.models import Order  # Assuming Order model exists or will be created
from users.models import Profile

class CustomAdminSite(admin.AdminSite):
    site_header = 'Luxerazo Admin'
    site_title = 'Luxerazo Admin Portal'
    index_title = 'Dashboard'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        # Placeholder data for dashboard metrics
        total_sales = Order.objects.aggregate(total=Sum('total_amount'))['total'] if hasattr(Order, 'total_amount') else 0
        total_orders = Order.objects.count() if hasattr(Order, 'id') else 0
        top_products = Product.objects.annotate(order_count=Count('id')).order_by('-order_count')[:5]
        top_brands = Brand.objects.annotate(product_count=Count('product')).order_by('-product_count')[:5]
        total_customers = Profile.objects.count()

        context = dict(
            self.each_context(request),
            total_sales=total_sales,
            total_orders=total_orders,
            top_products=top_products,
            top_brands=top_brands,
            total_customers=total_customers,
        )
        return TemplateResponse(request, "admin/dashboard.html", context)

custom_admin_site = CustomAdminSite(name='custom_admin')

# Register models with custom admin site
custom_admin_site.register(Product)
custom_admin_site.register(Brand)
custom_admin_site.register(Profile)
