from django.contrib import admin
from .models import Brand, Category, Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'price_in_usd', 'discount_percent', 'stock', 'gender')
    list_editable = ('price_in_usd', 'discount_percent', 'stock')
    list_filter = ('brand', 'category', 'gender', 'stock')
    search_fields = ('name', 'brand__name', 'category__name')

admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
