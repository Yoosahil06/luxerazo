from django.db import models

# Create your models here.
from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="brands/")

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/")
    description = models.TextField()
    price_in_usd = models.DecimalField(max_digits=10, decimal_places=2)
    authenticity = models.CharField(max_length=20, choices=[('Original', 'Original'), ('Grade-A', 'Grade-A')])
    stock = models.BooleanField(default=True)
    gender = models.CharField(max_length=10, choices=[('Men', 'Men'), ('Women', 'Women'), ('Unisex', 'Unisex')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
