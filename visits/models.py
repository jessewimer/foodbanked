# visits/models.py
from django.db import models
from accounts.models import Foodbank

class Patron(models.Model):
    foodbank = models.ForeignKey(Foodbank, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    zipcode = models.CharField(max_length=10)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.zipcode}"
    
    class Meta:
        ordering = ['last_name', 'first_name']


class Visit(models.Model):
    foodbank = models.ForeignKey(Foodbank, on_delete=models.CASCADE)
    patron = models.ForeignKey(Patron, on_delete=models.SET_NULL, null=True, blank=True)
    visit_date = models.DateField(auto_now_add=True)
    
    # Snapshot of patron info at time of visit
    patron_first_name = models.CharField(max_length=100, blank=True, null=True)
    patron_last_name = models.CharField(max_length=100, blank=True, null=True)
    patron_address = models.TextField(blank=True, null=True)
    zipcode = models.CharField(max_length=10)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    household_size = models.IntegerField()
    age_0_18 = models.IntegerField(default=0)  
    age_19_59 = models.IntegerField(default=0)
    age_60_plus = models.IntegerField(default=0)
    
    # First visit this month
    first_visit_this_month = models.BooleanField(default=False)

    comments = models.TextField(blank=True, null=True)

    is_food_truck = models.BooleanField(default=False)
    
    def __str__(self):
        patron_name = self.patron.name if self.patron else "Anonymous"
        return f"{patron_name} - {self.visit_date}"
    
    class Meta:
        ordering = ['-visit_date']