
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    loyalty_points = models.PositiveIntegerField(default=0)
    tier = models.CharField(max_length=20, default='Silver')

    def __str__(self):
        return f"{self.user.username} Profile"
