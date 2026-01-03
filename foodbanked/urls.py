"""
URL configuration for foodbanked project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""
URL configuration for foodbanked project.
"""
from django.contrib import admin
from django.urls import path, include
from . import views  # Import views from this file or wherever you put them

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Public pages
    path('', views.landing_page, name='landing'),
    path('demo/', views.demo_page, name='demo'),
    
    # App URLs
    path('accounts/', include('accounts.urls')),
    path('visits/', include('visits.urls')),
    path('patrons/', include('visits.urls')),  # Patron URLs can be in visits app
    path('stats/', include('visits.urls')),     # Stats URLs can be in visits app
    
    # Alternative: if you create separate URLs for different sections
    # path('dashboard/', views.dashboard, name='dashboard'),
]
