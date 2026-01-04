from django.contrib import admin
from .models import Foodbank, RegistrationCode


@admin.register(Foodbank)
class FoodbankAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'city', 'state', 'created_date']
    search_fields = ['name', 'city', 'user__username']
    list_filter = ['state', 'created_date']


@admin.register(RegistrationCode)
class RegistrationCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'is_used', 'used_by', 'used_date', 'created_date']
    search_fields = ['code', 'notes', 'used_by__username']
    list_filter = ['is_used', 'created_date']
    readonly_fields = ['used_by', 'used_date']
    
    fieldsets = (
        ('Code Information', {
            'fields': ('code', 'notes')
        }),
        ('Usage Status', {
            'fields': ('is_used', 'used_by', 'used_date')
        }),
    )