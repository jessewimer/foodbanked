from django.contrib.auth.models import User
from django.db import models

class Foodbank(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)  # e.g., "Moscow Food Bank"
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name