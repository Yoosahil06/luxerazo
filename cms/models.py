
from django.db import models

class Banner(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="banners/")
    active = models.BooleanField(default=True)

class Blog(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="blogs/")
    slug = models.SlugField(unique=True)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
