
from django.contrib.auth.models import User
from django.db import models
from products.models import Product

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    loyalty_points = models.PositiveIntegerField(default=0)
    tier = models.CharField(max_length=20, default='Silver')

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
