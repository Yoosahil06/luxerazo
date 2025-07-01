from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum
from .models import Product, Brand, Category, ProductImage, ProductVariant
import csv
from django.http import HttpResponse

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'variant', 'alt_text', 'is_main', 'order')

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0
    fields = ('name', 'sku', 'price_adjustment', 'stock_quantity', 'is_active', 'color', 'material', 'size')
    readonly_fields = ('created_at', 'updated_at')

def archive_products(modeladmin, request, queryset):
    """Archive selected products (soft delete)"""
    queryset.update(is_active=False)
    modeladmin.message_user(request, f"{queryset.count()} products have been archived.")
archive_products.short_description = "Archive selected products"

def activate_products(modeladmin, request, queryset):
    """Activate selected products"""
    queryset.update(is_active=True)
    modeladmin.message_user(request, f"{queryset.count()} products have been activated.")
activate_products.short_description = "Activate selected products"

def export_products_csv(modeladmin, request, queryset):
    """Export selected products to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Name', 'Brand', 'Category', 'Price USD', 'Discount %', 'Stock Quantity', 'Is Active', 'SKU'])
    
    for product in queryset:
        writer.writerow([
            product.name,
            product.brand.name,
            product.category.name,
            product.price_in_usd,
            product.discount_percent,
            product.stock_quantity,
            product.is_active,
            product.slug
        ])
    
    return response
export_products_csv.short_description = "Export selected products to CSV"

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'price_in_usd', 'discount_percent', 'total_stock', 'variant_count', 'stock_status', 'is_active', 'created_at')
    list_editable = ('price_in_usd', 'discount_percent', 'is_active')
    list_filter = ('brand', 'category', 'authenticity', 'is_active', 'gender', 'is_featured', 'created_at')
    search_fields = ('name', 'brand__name', 'category__name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductVariantInline, ProductImageInline]
    actions = [archive_products, activate_products, export_products_csv]
    change_list_template = 'admin/products/product/change_list.html'

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('bulk-upload/', self.admin_site.admin_view(self.bulk_upload_view), name='product_bulk_upload'),
        ]
        return custom_urls + urls

    def bulk_upload_view(self, request):
        from django.shortcuts import render
        from django.contrib import messages
        from django.http import HttpResponseRedirect
        from django.urls import reverse
        import csv
        import io

        if request.method == 'POST':
            csv_file = request.FILES.get('csv_file')
            if not csv_file:
                messages.error(request, 'Please upload a CSV file.')
                return HttpResponseRedirect(request.path_info)

            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'Please upload a valid CSV file.')
                return HttpResponseRedirect(request.path_info)

            # Read the CSV file
            try:
                csv_file = csv_file.read().decode('utf-8')
                csv_data = csv.DictReader(io.StringIO(csv_file))
                
                # Call the bulk upload command
                from django.core.management import call_command
                from io import StringIO
                import tempfile
                import os

                # Create a temporary file to store the CSV
                with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='') as temp_file:
                    writer = csv.DictWriter(temp_file, fieldnames=csv_data.fieldnames)
                    writer.writeheader()
                    for row in csv_data:
                        writer.writerow(row)
                    temp_file_path = temp_file.name

                try:
                    # Capture command output
                    out = StringIO()
                    call_command('bulk_upload_products', temp_file_path, stdout=out)
                    messages.success(request, out.getvalue())
                except Exception as e:
                    messages.error(request, f'Error during bulk upload: {str(e)}')
                finally:
                    # Clean up temporary file
                    os.unlink(temp_file_path)

            except Exception as e:
                messages.error(request, f'Error processing CSV file: {str(e)}')
            
            return HttpResponseRedirect(reverse('admin:products_product_changelist'))

        return render(request, 'admin/products/product/bulk_upload.html', {
            'title': 'Bulk Upload Products',
            'opts': self.model._meta,
        })
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'brand', 'category', 'description')
        }),
        ('Pricing', {
            'fields': ('price_in_usd', 'discount_percent')
        }),
        ('Product Details', {
            'fields': ('authenticity', 'materials', 'dimensions', 'care_instructions', 'story')
        }),
        ('Inventory & Status', {
            'fields': ('stock_quantity', 'is_active', 'is_featured', 'stock', 'gender')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        })
    )

    def total_stock(self, obj):
        """Calculate total stock including variants"""
        variant_stock = obj.variants.aggregate(total=Sum('stock_quantity'))['total'] or 0
        return obj.stock_quantity + variant_stock
    total_stock.short_description = 'Total Stock'

    def variant_count(self, obj):
        """Count number of variants"""
        return obj.variants.count()
    variant_count.short_description = 'Variants'

    def stock_status(self, obj):
        """Display stock status with color coding"""
        total = self.total_stock(obj)
        if total == 0:
            return format_html('<span style="color: red;">Out of Stock</span>')
        elif total <= 5:
            return format_html('<span style="color: orange;">Low Stock ({})</span>', total)
        else:
            return format_html('<span style="color: green;">In Stock ({})</span>', total)
    stock_status.short_description = 'Stock Status'

class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'sku', 'final_price', 'stock_quantity', 'is_active', 'created_at')
    list_filter = ('is_active', 'color', 'material', 'size', 'created_at')
    search_fields = ('product__name', 'name', 'sku', 'color', 'material')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('product', 'name', 'sku', 'price_adjustment')
        }),
        ('Inventory', {
            'fields': ('stock_quantity', 'is_active')
        }),
        ('Variant Attributes', {
            'fields': ('color', 'material', 'size', 'weight')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'is_active', 'created_at')
    list_filter = ('is_active', 'parent')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductImage)
