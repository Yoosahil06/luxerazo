from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from products.models import Product
from orders.models import Order

User = get_user_model()

class SalesReport(models.Model):
    PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ]

    period = models.CharField(max_length=20, choices=PERIOD_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    total_orders = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_items_sold = models.IntegerField(default=0)
    average_order_value = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    new_customers = models.IntegerField(default=0)
    returning_customers = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['period', 'start_date', 'end_date']
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.period.title()} Report: {self.start_date} to {self.end_date}"

class ProductAnalytics(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='analytics')
    date = models.DateField()
    views = models.IntegerField(default=0)
    add_to_cart = models.IntegerField(default=0)
    purchases = models.IntegerField(default=0)
    revenue = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    conversion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        unique_together = ['product', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.product.name} - {self.date}"

    def save(self, *args, **kwargs):
        if self.views > 0:
            self.conversion_rate = (self.purchases / self.views) * 100
        super().save(*args, **kwargs)

class CustomerInsight(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='insights')
    total_orders = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    average_order_value = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    first_purchase_date = models.DateTimeField(null=True, blank=True)
    last_purchase_date = models.DateTimeField(null=True, blank=True)
    favorite_category = models.CharField(max_length=100, blank=True)
    favorite_brand = models.CharField(max_length=100, blank=True)
    customer_lifetime_value = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    purchase_frequency = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # orders per month
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Insights for {self.user.username}"

    def update_insights(self):
        """Update customer insights based on order history"""
        orders = Order.objects.filter(user=self.user, status='delivered')
        
        if orders.exists():
            self.total_orders = orders.count()
            self.total_spent = sum(order.total for order in orders)
            self.average_order_value = self.total_spent / self.total_orders if self.total_orders > 0 else 0
            self.first_purchase_date = orders.order_by('created_at').first().created_at
            self.last_purchase_date = orders.order_by('-created_at').first().created_at
            
            # Calculate purchase frequency (orders per month)
            if self.first_purchase_date:
                months_active = max(1, (timezone.now() - self.first_purchase_date).days / 30)
                self.purchase_frequency = self.total_orders / months_active
            
            # Calculate CLV (simplified: total_spent * purchase_frequency * 12)
            self.customer_lifetime_value = self.total_spent * (self.purchase_frequency or 1) * 12
            
        self.save()

class TrafficSource(models.Model):
    SOURCE_CHOICES = [
        ('direct', 'Direct'),
        ('google', 'Google Search'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('email', 'Email Campaign'),
        ('referral', 'Referral'),
        ('paid_ads', 'Paid Ads'),
    ]

    source = models.CharField(max_length=50, choices=SOURCE_CHOICES)
    date = models.DateField()
    visitors = models.IntegerField(default=0)
    page_views = models.IntegerField(default=0)
    sessions = models.IntegerField(default=0)
    bounce_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    conversion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    revenue = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        unique_together = ['source', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.get_source_display()} - {self.date}"

class ConversionFunnel(models.Model):
    date = models.DateField()
    visitors = models.IntegerField(default=0)
    product_views = models.IntegerField(default=0)
    add_to_cart = models.IntegerField(default=0)
    checkout_started = models.IntegerField(default=0)
    orders_completed = models.IntegerField(default=0)
    
    # Calculated rates
    product_view_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    add_to_cart_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    checkout_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    completion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    overall_conversion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Conversion Funnel - {self.date}"

    def save(self, *args, **kwargs):
        # Calculate conversion rates
        if self.visitors > 0:
            self.product_view_rate = (self.product_views / self.visitors) * 100
            self.overall_conversion_rate = (self.orders_completed / self.visitors) * 100
        
        if self.product_views > 0:
            self.add_to_cart_rate = (self.add_to_cart / self.product_views) * 100
        
        if self.add_to_cart > 0:
            self.checkout_rate = (self.checkout_started / self.add_to_cart) * 100
        
        if self.checkout_started > 0:
            self.completion_rate = (self.orders_completed / self.checkout_started) * 100
        
        super().save(*args, **kwargs)

class TopSellingProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    period_start = models.DateField()
    period_end = models.DateField()
    units_sold = models.IntegerField(default=0)
    revenue = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    rank = models.IntegerField(default=0)

    class Meta:
        ordering = ['rank', '-revenue']

    def __str__(self):
        return f"#{self.rank} {self.product.name} ({self.period_start} - {self.period_end})"
