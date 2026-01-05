# visits/models.py
from django.db import models
from accounts.models import Foodbank

class Patron(models.Model):
    foodbank = models.ForeignKey(Foodbank, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True, null=True)
    zipcode = models.CharField(max_length=10)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.zipcode}"
    
    class Meta:
        ordering = ['name']


class Visit(models.Model):
    foodbank = models.ForeignKey(Foodbank, on_delete=models.CASCADE)
    patron = models.ForeignKey(Patron, on_delete=models.SET_NULL, null=True, blank=True)
    visit_date = models.DateField(auto_now_add=True)
    
    # Required fields
    zipcode = models.CharField(max_length=10)
    household_size = models.IntegerField()
    
    # Age group counts (adjust ranges as needed)
    # age_0_17 = models.IntegerField(default=0)
    # age_18_30 = models.IntegerField(default=0)
    # age_31_50 = models.IntegerField(default=0)
    # age_51_plus = models.IntegerField(default=0)
    age_0_18 = models.IntegerField(default=0)  
    age_19_59 = models.IntegerField(default=0)
    age_60_plus = models.IntegerField(default=0)
    
    # First visit this month
    first_visit_this_month = models.BooleanField(default=False)
    
    def __str__(self):
        patron_name = self.patron.name if self.patron else "Anonymous"
        return f"{patron_name} - {self.visit_date}"
    
    class Meta:
        ordering = ['-visit_date']