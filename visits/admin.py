from django.contrib import admin
from .models import Patron, Visit

@admin.register(Patron)
class PatronAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'zipcode', 'city', 'state', 'foodbank', 'created_date')
    search_fields = ('first_name', 'last_name', 'name', 'zipcode', 'phone')
    list_filter = ('foodbank', 'state', 'city', 'created_date')
    readonly_fields = ('created_date',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'name')
        }),
        ('Contact Information', {
            'fields': ('address', 'zipcode', 'city', 'state', 'phone')
        }),
        ('Food Bank', {
            'fields': ('foodbank',)
        }),
        ('Additional Information', {
            'fields': ('comments', 'created_date')
        }),
    )

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('visit_date', 'patron_display', 'foodbank', 'zipcode', 'household_size', 'first_visit_this_month', 'is_food_truck')
    search_fields = ('patron_first_name', 'patron_last_name', 'zipcode', 'patron__first_name', 'patron__last_name')
    list_filter = ('foodbank', 'visit_date', 'first_visit_this_month', 'is_food_truck', 'state')
    readonly_fields = ('visit_date',)
    date_hierarchy = 'visit_date'
    
    fieldsets = (
        ('Visit Information', {
            'fields': ('foodbank', 'patron', 'visit_date', 'first_visit_this_month', 'is_food_truck')
        }),
        ('Patron Snapshot', {
            'fields': ('patron_first_name', 'patron_last_name', 'patron_address', 'zipcode', 'city', 'state')
        }),
        ('Household Demographics', {
            'fields': ('household_size', 'age_0_18', 'age_19_59', 'age_60_plus')
        }),
        ('Additional Information', {
            'fields': ('comments',)
        }),
    )
    
    def patron_display(self, obj):
        if obj.patron:
            return f"{obj.patron.first_name} {obj.patron.last_name}"
        return f"{obj.patron_first_name or ''} {obj.patron_last_name or 'Anonymous'}".strip() or "Anonymous"
    patron_display.short_description = 'Patron'