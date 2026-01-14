from django.db import models


class FoodItem(models.Model):
    """
    Food items with shelf life information for food bank reference.
    Used in the Shelf Life tool to help food banks make informed decisions
    about food safety and reduce waste.
    """
    
    CATEGORY_CHOICES = [
        ('baby_food', 'Baby Food'),
        ('shelf_stable', 'Shelf-Stable'),
        ('refrigerated', 'Refrigerated'),
        ('frozen', 'Frozen'),
    ]
    
    name = models.CharField(max_length=255, db_index=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, db_index=True)
    subcategory = models.CharField(max_length=100, blank=True)
    
    # Display string shown to users (e.g., "2-3 months", "Expiration date on package")
    shelf_life_display = models.CharField(max_length=100)
    
    # Numeric values for calculations (in days)
    # None/null means "use expiration date on package"
    shelf_life_min_days = models.IntegerField(null=True, blank=True)
    shelf_life_max_days = models.IntegerField(null=True, blank=True)
    
    # Additional notes or special handling instructions
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Food Item'
        verbose_name_plural = 'Food Items'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
    
    def has_numeric_shelf_life(self):
        """Returns True if this item has calculable shelf life (not just 'use expiration date')"""
        return self.shelf_life_min_days is not None and self.shelf_life_max_days is not None