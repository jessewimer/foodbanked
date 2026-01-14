from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .models import FoodItem


@login_required
def shelf_life(request):
    """Main shelf life search page"""
    return render(request, 'resources/shelf_life.html')


@login_required
def search_food_items(request):
    """
    API endpoint for autocomplete search
    Searches in name, category, and subcategory
    Returns results grouped by category
    """
    query = request.GET.get('q', '').strip()
    
    # Require at least 2 characters to search
    if len(query) < 2:
        return JsonResponse({'results': {}})
    
    # Search in name, category display, and subcategory
    items = FoodItem.objects.filter(
        Q(name__icontains=query) |
        Q(subcategory__icontains=query)
    ).select_related().order_by('category', 'name')[:50]  # Limit to 50 results
    
    # Group results by category
    results_by_category = {}
    category_order = ['baby_food', 'shelf_stable', 'refrigerated', 'frozen']
    
    for item in items:
        category_display = item.get_category_display()
        
        if category_display not in results_by_category:
            results_by_category[category_display] = []
        
        results_by_category[category_display].append({
            'id': item.id,
            'name': item.name,
            'category': item.category,
            'category_display': category_display,
            'subcategory': item.subcategory,
            'shelf_life': item.shelf_life_display,
        })
    
    # Return results in category order
    ordered_results = {}
    for cat_key in category_order:
        cat_display = dict(FoodItem.CATEGORY_CHOICES).get(cat_key)
        if cat_display in results_by_category:
            ordered_results[cat_display] = results_by_category[cat_display]
    
    return JsonResponse({
        'results': ordered_results,
        'total': sum(len(items) for items in ordered_results.values())
    })


@login_required
def get_food_item_detail(request, item_id):
    """
    Get detailed information about a specific food item
    Returns data for the popup modal
    """
    item = get_object_or_404(FoodItem, id=item_id)
    
    # Determine category icon
    category_icons = {
        'baby_food': '🍼',
        'shelf_stable': '🥫',
        'refrigerated': '❄️',
        'frozen': '🧊'
    }
    
    data = {
        'id': item.id,
        'name': item.name,
        'category': item.category,
        'category_display': item.get_category_display(),
        'category_icon': category_icons.get(item.category, '📦'),
        'subcategory': item.subcategory,
        'shelf_life_display': item.shelf_life_display,
        'shelf_life_min_days': item.shelf_life_min_days,
        'shelf_life_max_days': item.shelf_life_max_days,
        'has_numeric_shelf_life': item.has_numeric_shelf_life(),
        'notes': item.notes,
    }
    
    return JsonResponse(data)