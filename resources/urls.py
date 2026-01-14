from django.urls import path
from . import views

app_name = 'resources'

urlpatterns = [

    path('shelf-life/', views.shelf_life, name='shelf_life'),

    # API endpoints
    path('search/', views.search_food_items, name='search_food_items'),
    path('item/<int:item_id>/', views.get_food_item_detail, name='food_item_detail'),

]