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
    email = models.EmailField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    food_truck_enabled = models.BooleanField(default=False)
    timezone = models.CharField(max_length=50, default='America/Los_Angeles')
    
    def __str__(self):
        return self.name
    
class RegistrationCode(models.Model):
    """Registration codes for controlling who can sign up"""
    code = models.CharField(max_length=50, unique=True)
    is_used = models.BooleanField(default=False)
    used_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    used_date = models.DateTimeField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, help_text="Optional notes about who this code is for")
    
    def __str__(self):
        return f"{self.code} ({'Used' if self.is_used else 'Available'})"
    
    class Meta:
        ordering = ['-created_date']

class ServiceZipcode(models.Model):
    """Service area zip codes for a food bank"""
    foodbank = models.ForeignKey(Foodbank, on_delete=models.CASCADE, related_name='service_zipcodes')
    zipcode = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)  # Two-letter state code
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['zipcode']
    
    def __str__(self):
        return f"{self.zipcode} - {self.city}, {self.state}"