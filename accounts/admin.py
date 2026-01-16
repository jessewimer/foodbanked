# from django.contrib import admin
# from .models import FoodbankOrganization, OrganizationAdmin, Foodbank, FoodbankUser, RegistrationCode

# @admin.register(FoodbankOrganization)
# class FoodbankOrganizationAdmin(admin.ModelAdmin):
#     list_display = ('name', 'region', 'city', 'state', 'email', 'created_date')
#     search_fields = ('name', 'region', 'city')
#     list_filter = ('state', 'created_date')

# @admin.register(OrganizationAdmin)
# class OrganizationAdminAdmin(admin.ModelAdmin):
#     list_display = ('user', 'organization', 'created_date')
#     search_fields = ('user__username', 'organization__name')
#     list_filter = ('organization', 'created_date')

# @admin.register(Foodbank)
# class FoodbankAdmin(admin.ModelAdmin):
#     list_display = ('name', 'organization', 'city', 'state', 'food_truck_enabled', 'created_date')
#     search_fields = ('name', 'city')
#     list_filter = ('organization', 'state', 'food_truck_enabled')

# @admin.register(FoodbankUser)
# class FoodbankUserAdmin(admin.ModelAdmin):
#     list_display = ('user', 'foodbank', 'role', 'created_date')
#     search_fields = ('user__username', 'foodbank__name')
#     list_filter = ('role', 'foodbank', 'created_date')


# @admin.register(RegistrationCode)
# class RegistrationCodeAdmin(admin.ModelAdmin):
#     list_display = ['code', 'is_used', 'used_by', 'used_date', 'created_date']
#     search_fields = ['code', 'notes', 'used_by__username']
#     list_filter = ['is_used', 'created_date']
#     readonly_fields = ['used_by', 'used_date']
    
#     fieldsets = (
#         ('Code Information', {
#             'fields': ('code', 'notes')
#         }),
#         ('Usage Status', {
#             'fields': ('is_used', 'used_by', 'used_date')
#         }),
#     )

from django.contrib import admin
from .models import FoodbankOrganization, OrganizationAdmin, Foodbank, RegistrationCode, ServiceZipcode

@admin.register(FoodbankOrganization)
class FoodbankOrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'region', 'city', 'state', 'email', 'created_date')
    search_fields = ('name', 'slug', 'region', 'city')
    list_filter = ('state', 'created_date')

@admin.register(OrganizationAdmin)
class OrganizationAdminAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'created_date')
    search_fields = ('user__username', 'organization__name')
    list_filter = ('organization', 'created_date')

@admin.register(Foodbank)
class FoodbankAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'city', 'state', 'food_truck_enabled', 'created_date')
    search_fields = ('name', 'city', 'user__username')
    list_filter = ('organization', 'state', 'food_truck_enabled', 'created_date')

@admin.register(RegistrationCode)
class RegistrationCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'is_used', 'used_by', 'used_date', 'created_date')
    search_fields = ('code', 'notes', 'used_by__username')
    list_filter = ('is_used', 'created_date')

@admin.register(ServiceZipcode)
class ServiceZipcodeAdmin(admin.ModelAdmin):
    list_display = ('zipcode', 'city', 'state', 'foodbank', 'created_date')
    search_fields = ('zipcode', 'city', 'foodbank__name')
    list_filter = ('state', 'foodbank')