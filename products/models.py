from django.db import models
from django.urls import reverse

class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, default='default-slug')
    logo = models.ImageField(upload_to="brands/", blank=True, null=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:brand_detail', kwargs={'slug': self.slug})

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, default='default-category-slug')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:category_detail', kwargs={'slug': self.slug})

class Product(models.Model):
    AUTHENTICITY_CHOICES = [
        ('original', '100% Certified Original'),
        ('grade_a', 'Grade-A First Copy'),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, default='default-product-slug')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    price_in_usd = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    authenticity = models.CharField(max_length=20, choices=AUTHENTICITY_CHOICES, default='original')
    
    # Enhanced product details
    materials = models.TextField(blank=True)
    dimensions = models.CharField(max_length=200, blank=True)
    care_instructions = models.TextField(blank=True)
    story = models.TextField(blank=True)
    
    # Inventory
    stock_quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # Legacy fields
    stock = models.BooleanField(default=True)
    gender = models.CharField(max_length=10, choices=[('Men', 'Men'), ('Women', 'Women'), ('Unisex', 'Unisex')], default='Unisex')
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:product_detail', kwargs={'slug': self.slug})

    @property
    def discounted_price(self):
        if self.discount_percent > 0:
            discount_amount = self.price_in_usd * (self.discount_percent / 100)
            return self.price_in_usd - discount_amount
        return self.price_in_usd

    @property
    def is_in_stock(self):
        return self.stock_quantity > 0

    @property
    def main_image(self):
        return self.images.filter(is_main=True).first()

    @property
    def thumbnail_images(self):
        return self.images.filter(is_main=False)[:5]

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=100)  # e.g., "Rose Gold", "Steel"
    sku = models.CharField(max_length=100, unique=True)
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock_quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    # Variant specific attributes
    color = models.CharField(max_length=50, blank=True)
    material = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=50, blank=True)
    weight = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        unique_together = ['product', 'name']

    def __str__(self):
        return f"{self.product.name} - {self.name}"

    @property
    def final_price(self):
        """Calculate final price including base product price and variant adjustment"""
        return self.product.price_in_usd + self.price_adjustment

    @property
    def is_in_stock(self):
        return self.stock_quantity > 0

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_main = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.product.name} - Image {self.order}"
