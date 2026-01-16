
# accounts/models.py
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class FoodbankOrganization(models.Model):
    """Parent organization that manages multiple foodbanks"""
    name = models.CharField(max_length=200)  # e.g., "Idaho Foodbank"
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    region = models.CharField(max_length=100, blank=True, null=True)  # e.g., "Idaho", "Eastern Washington"
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    # New fields for locations map
    description = models.TextField(
        blank=True, 
        null=True, 
        help_text="Public description for your organization (shown on locations page)"
    )
    is_public = models.BooleanField(
        default=False, 
        help_text="Show on public locations map"
    )
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        help_text="Auto-generated from address"
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        help_text="Auto-generated from address"
    )
    
    def save(self, *args, **kwargs):
        # Auto-generate slug from name if not set
        if not self.slug:
            self.slug = slugify(self.name)
        
        # Check if we need to geocode
        needs_geocoding = False
        
        if not self.pk:
            # New record - geocode if we have address info
            needs_geocoding = True
        elif not self.latitude or not self.longitude:
            # Missing coordinates - geocode
            needs_geocoding = True
        else:
            # Check if address changed for existing record
            try:
                old = FoodbankOrganization.objects.get(pk=self.pk)
                if (old.address != self.address or 
                    old.city != self.city or 
                    old.state != self.state or 
                    old.zipcode != self.zipcode):
                    needs_geocoding = True
            except FoodbankOrganization.DoesNotExist:
                needs_geocoding = True
        
        if needs_geocoding:
            self.geocode()
        
        super().save(*args, **kwargs)
    
    def geocode(self):
        """Geocode this organization's address"""
        from foodbanked.geocoding import geocode_address
        lat, lng = geocode_address(self.address, self.city, self.state, self.zipcode)
        if lat and lng:
            self.latitude = lat
            self.longitude = lng
    
    def __str__(self):
        return self.name


class Foodbank(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(
        FoodbankOrganization, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='foodbanks',
        help_text="Parent organization, if part of a larger network"
    )
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
    allow_by_name = models.BooleanField(default=True)
    allow_anonymous = models.BooleanField(default=True)
    
    # New fields for locations map
    description = models.TextField(
        blank=True, 
        null=True, 
        help_text="Tell people about your food bank (shown on locations page)"
    )
    is_public = models.BooleanField(
        default=False, 
        help_text="Show on public locations map"
    )
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        help_text="Auto-generated from address"
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        help_text="Auto-generated from address"
    )
    
    def save(self, *args, **kwargs):
        # Check if we need to geocode
        needs_geocoding = False
        
        if not self.pk:
            # New record - geocode if we have address info
            needs_geocoding = True
        elif not self.latitude or not self.longitude:
            # Missing coordinates - geocode
            needs_geocoding = True
        else:
            # Check if address changed for existing record
            try:
                old = Foodbank.objects.get(pk=self.pk)
                if (old.address != self.address or 
                    old.city != self.city or 
                    old.state != self.state or 
                    old.zipcode != self.zipcode):
                    needs_geocoding = True
            except Foodbank.DoesNotExist:
                needs_geocoding = True
        
        if needs_geocoding:
            self.geocode()
        
        super().save(*args, **kwargs)
    
    def geocode(self):
        """Geocode this foodbank's address"""
        from foodbanked.geocoding import geocode_address
        lat, lng = geocode_address(self.address, self.city, self.state, self.zipcode)
        if lat and lng:
            self.latitude = lat
            self.longitude = lng
    
    def __str__(self):
        return self.name












# class FoodbankOrganization(models.Model):
#     """Parent organization that manages multiple foodbanks"""
#     name = models.CharField(max_length=200)  # e.g., "Idaho Foodbank"
#     slug = models.SlugField(max_length=200, unique=True, blank=True)
#     region = models.CharField(max_length=100, blank=True, null=True)  # e.g., "Idaho", "Eastern Washington"
#     address = models.CharField(max_length=200, blank=True, null=True)
#     city = models.CharField(max_length=100, blank=True, null=True)
#     state = models.CharField(max_length=2, blank=True, null=True)
#     zipcode = models.CharField(max_length=10, blank=True, null=True)
#     phone = models.CharField(max_length=20, blank=True, null=True)
#     email = models.EmailField(blank=True, null=True)  # Changed from contact_email
#     website = models.URLField(max_length=200, blank=True, null=True)
#     created_date = models.DateTimeField(auto_now_add=True)

    
#     def __str__(self):
#         return self.name

class OrganizationAdmin(models.Model):
    """Admin users who can see data across all foodbanks in their organization"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(FoodbankOrganization, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.organization.name}"

# class Foodbank(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     organization = models.ForeignKey(
#         FoodbankOrganization, 
#         on_delete=models.SET_NULL, 
#         null=True, 
#         blank=True,
#         related_name='foodbanks',
#         help_text="Parent organization, if part of a larger network"
#     )
#     name = models.CharField(max_length=200)  # e.g., "Moscow Food Bank"
#     address = models.TextField(blank=True)
#     city = models.CharField(max_length=100, blank=True)
#     state = models.CharField(max_length=2, blank=True)
#     zipcode = models.CharField(max_length=10, blank=True)
#     phone = models.CharField(max_length=20, blank=True)
#     email = models.EmailField(blank=True)
#     created_date = models.DateTimeField(auto_now_add=True)
#     food_truck_enabled = models.BooleanField(default=False)
#     timezone = models.CharField(max_length=50, default='America/Los_Angeles')

#     allow_by_name = models.BooleanField(default=True)
#     allow_anonymous = models.BooleanField(default=True)
    
#     def __str__(self):
#         return self.name
    
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