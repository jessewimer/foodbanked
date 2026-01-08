"""
URL configuration for accounts app.
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    
    # Account settings
    path('settings/', views.account_settings, name='account_settings'),
    path('settings/add-zipcode/', views.add_zipcode, name='add_zipcode'),
    path('settings/delete-zipcode/<int:pk>/', views.delete_zipcode, name='delete_zipcode'),
    path('settings/toggle-food-truck/', views.toggle_food_truck, name='toggle_food_truck'),

]