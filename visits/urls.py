from django.urls import path
from . import views

app_name = 'visits'

urlpatterns = [
    # Visits
    path('visits/', views.visit_list, name='visit_list'),
    path('visits/new/', views.visit_create, name='visit_create'),
    path('visits/<int:pk>/', views.visit_detail, name='visit_detail'),
    path('visits/<int:pk>/delete/', views.visit_delete, name='visit_delete'),
    
    # Patrons
    path('patrons/', views.patron_list, name='patron_list'),
    path('patrons/new/', views.patron_create, name='patron_create'),
    path('patrons/<int:pk>/', views.patron_detail, name='patron_detail'),
    path('patrons/<int:pk>/delete/', views.patron_delete, name='patron_delete'),
    
    # AJAX endpoint for editing patron from visit form
    path('patron/<int:pk>/edit-ajax/', views.patron_edit_ajax, name='patron_edit_ajax'),

    path('api/patron/<int:patron_id>/', views.patron_detail_api, name='patron_detail_api'),
    
    # Stats
    path('analytics/', views.analytics_view, name='analytics'),
]