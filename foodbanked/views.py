from django.shortcuts import render, get_object_or_404
import json
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from accounts.models import Foodbank, FoodbankOrganization
from django.db.models import Q


def landing_page(request):
    """Public landing page view"""
    return render(request, 'landing.html')


def demo_page(request):
    """Interactive demo page where users can try the app without logging in"""
    
    # Calculate dates for visit history
    today = datetime.now().date()
    
    # Mock patrons with visit history - 40 patrons with varied data
    mock_patrons = [
        # Frequent visitors (3+ visits this month)
        {
            'id': 1, 
            'first_name': 'Sarah', 
            'last_name': 'Johnson', 
            'address': '456 Oak Avenue', 
            'zipcode': '83844',
            'phone': '(360) 555-0101',
            'visits_this_month': 4,
            'last_visit_date': (today - timedelta(days=2)).isoformat(),
            'last_visit': {
                'zipcode': '83844',
                'household_size': 3,
                'age_0_18': 1,
                'age_19_59': 2,
                'age_60_plus': 0
            }
        },
        {
            'id': 2, 
            'first_name': 'Michael', 
            'last_name': 'Brown', 
            'address': '789 Pine Road', 
            'zipcode': '83843',
            'phone': '(360) 555-0102',
            'visits_this_month': 3,
            'last_visit_date': (today - timedelta(days=5)).isoformat(),
            'last_visit': {
                'zipcode': '83843',
                'household_size': 5,
                'age_0_18': 2,
                'age_19_59': 2,
                'age_60_plus': 1
            }
        },
        {
            'id': 3, 
            'first_name': 'Maria', 
            'last_name': 'Garcia', 
            'address': '987 Cedar Lane', 
            'zipcode': '83844',
            'phone': '(360) 555-0103',
            'visits_this_month': 3,
            'last_visit_date': (today - timedelta(days=7)).isoformat(),
            'last_visit': {
                'zipcode': '83844',
                'household_size': 4,
                'age_0_18': 2,
                'age_19_59': 2,
                'age_60_plus': 0
            }
        },
        
        # Regular visitors (2 visits this month)
        {
            'id': 4, 
            'first_name': 'John', 
            'last_name': 'Smith', 
            'address': '123 Main St', 
            'zipcode': '83843',
            'phone': '(360) 555-0104',
            'visits_this_month': 2,
            'last_visit_date': (today - timedelta(days=10)).isoformat(),
            'last_visit': {
                'zipcode': '83843',
                'household_size': 2,
                'age_0_18': 0,
                'age_19_59': 2,
                'age_60_plus': 0
            }
        },
        {
            'id': 5, 
            'first_name': 'Emily', 
            'last_name': 'Davis', 
            'address': '321 Elm Street', 
            'zipcode': '83845',
            'phone': '(360) 555-0105',
            'visits_this_month': 2,
            'last_visit_date': (today - timedelta(days=12)).isoformat(),
            'last_visit': {
                'zipcode': '83845',
                'household_size': 1,
                'age_0_18': 0,
                'age_19_59': 1,
                'age_60_plus': 0
            }
        },
        {
            'id': 6, 
            'first_name': 'David', 
            'last_name': 'Wilson', 
            'address': '654 Maple Drive', 
            'zipcode': '83843',
            'phone': '(360) 555-0106',
            'visits_this_month': 2,
            'last_visit_date': (today - timedelta(days=8)).isoformat(),
            'last_visit': {
                'zipcode': '83843',
                'household_size': 3,
                'age_0_18': 1,
                'age_19_59': 1,
                'age_60_plus': 1
            }
        },
        {
            'id': 7, 
            'first_name': 'Lisa', 
            'last_name': 'Anderson', 
            'address': '258 Spruce Way', 
            'zipcode': '83843',
            'phone': '(360) 555-0107',
            'visits_this_month': 2,
            'last_visit_date': (today - timedelta(days=14)).isoformat(),
            'last_visit': {
                'zipcode': '83843',
                'household_size': 4,
                'age_0_18': 2,
                'age_19_59': 2,
                'age_60_plus': 0
            }
        },
        
        # First-time visitors this month (1 visit)
        {
            'id': 8, 
            'first_name': 'James', 
            'last_name': 'Martinez', 
            'address': '147 Birch Court', 
            'zipcode': '83846',
            'phone': '(360) 555-0108',
            'visits_this_month': 1,
            'last_visit_date': (today - timedelta(days=20)).isoformat(),
            'last_visit': {
                'zipcode': '83846',
                'household_size': 6,
                'age_0_18': 3,
                'age_19_59': 2,
                'age_60_plus': 1
            }
        },
        {
            'id': 9, 
            'first_name': 'Robert', 
            'last_name': 'Taylor', 
            'address': '369 Willow Path', 
            'zipcode': '83844',
            'phone': '(360) 555-0109',
            'visits_this_month': 1,
            'last_visit_date': (today - timedelta(days=18)).isoformat(),
            'last_visit': {
                'zipcode': '83844',
                'household_size': 2,
                'age_0_18': 0,
                'age_19_59': 1,
                'age_60_plus': 1
            }
        },
        {
            'id': 10, 
            'first_name': 'Jennifer', 
            'last_name': 'Thomas', 
            'address': '741 Aspen Boulevard', 
            'zipcode': '83845',
            'phone': '(360) 555-0110',
            'visits_this_month': 1,
            'last_visit_date': (today - timedelta(days=15)).isoformat(),
            'last_visit': {
                'zipcode': '83845',
                'household_size': 3,
                'age_0_18': 1,
                'age_19_59': 2,
                'age_60_plus': 0
            }
        },
        
        # More patrons for varied searching
        {'id': 11, 'first_name': 'William', 'last_name': 'Moore', 'address': '852 Hickory Street', 'zipcode': '83843', 'phone': '(360) 555-0111', 'visits_this_month': 1, 'last_visit_date': (today - timedelta(days=22)).isoformat(), 'last_visit': {'zipcode': '83843', 'household_size': 4, 'age_0_18': 2, 'age_19_59': 1, 'age_60_plus': 1}},
        {'id': 12, 'first_name': 'Patricia', 'last_name': 'Jackson', 'address': '963 Poplar Avenue', 'zipcode': '83846', 'phone': '(360) 555-0112', 'visits_this_month': 2, 'last_visit_date': (today - timedelta(days=9)).isoformat(), 'last_visit': {'zipcode': '83846', 'household_size': 2, 'age_0_18': 0, 'age_19_59': 2, 'age_60_plus': 0}},
        {'id': 13, 'first_name': 'Christopher', 'last_name': 'White', 'address': '159 Dogwood Lane', 'zipcode': '83843', 'phone': '(360) 555-0113', 'visits_this_month': 1, 'last_visit_date': (today - timedelta(days=25)).isoformat(), 'last_visit': {'zipcode': '83843', 'household_size': 5, 'age_0_18': 3, 'age_19_59': 2, 'age_60_plus': 0}},
        {'id': 14, 'first_name': 'Linda', 'last_name': 'Harris', 'address': '753 Magnolia Drive', 'zipcode': '83844', 'phone': '(360) 555-0114', 'visits_this_month': 0, 'last_visit_date': None, 'last_visit': None},
        {'id': 15, 'first_name': 'Daniel', 'last_name': 'Martin', 'address': '246 Redwood Court', 'zipcode': '83845', 'phone': '(360) 555-0115', 'visits_this_month': 3, 'last_visit_date': (today - timedelta(days=4)).isoformat(), 'last_visit': {'zipcode': '83845', 'household_size': 3, 'age_0_18': 1, 'age_19_59': 2, 'age_60_plus': 0}},
        {'id': 16, 'first_name': 'Nancy', 'last_name': 'Thompson', 'address': '135 Sycamore Street', 'zipcode': '83843', 'phone': '(360) 555-0116', 'visits_this_month': 1, 'last_visit_date': (today - timedelta(days=19)).isoformat(), 'last_visit': {'zipcode': '83843', 'household_size': 1, 'age_0_18': 0, 'age_19_59': 0, 'age_60_plus': 1}},
        {'id': 17, 'first_name': 'Matthew', 'last_name': 'Robinson', 'address': '468 Beech Road', 'zipcode': '83846', 'phone': '(360) 555-0117', 'visits_this_month': 2, 'last_visit_date': (today - timedelta(days=11)).isoformat(), 'last_visit': {'zipcode': '83846', 'household_size': 4, 'age_0_18': 2, 'age_19_59': 2, 'age_60_plus': 0}},
        {'id': 18, 'first_name': 'Betty', 'last_name': 'Clark', 'address': '791 Walnut Avenue', 'zipcode': '83844', 'phone': '(360) 555-0118', 'visits_this_month': 0, 'last_visit_date': None, 'last_visit': None},
        {'id': 19, 'first_name': 'Anthony', 'last_name': 'Rodriguez', 'address': '357 Chestnut Place', 'zipcode': '83843', 'phone': '(360) 555-0119', 'visits_this_month': 4, 'last_visit_date': (today - timedelta(days=3)).isoformat(), 'last_visit': {'zipcode': '83843', 'household_size': 5, 'age_0_18': 2, 'age_19_59': 2, 'age_60_plus': 1}},
        {'id': 20, 'first_name': 'Sandra', 'last_name': 'Lewis', 'address': '912 Cottonwood Way', 'zipcode': '83845', 'phone': '(360) 555-0120', 'visits_this_month': 1, 'last_visit_date': (today - timedelta(days=17)).isoformat(), 'last_visit': {'zipcode': '83845', 'household_size': 2, 'age_0_18': 0, 'age_19_59': 2, 'age_60_plus': 0}},
        
        # Additional patrons for robust search testing
        {'id': 21, 'first_name': 'Mark', 'last_name': 'Walker', 'address': '234 Hemlock Lane', 'zipcode': '83843', 'phone': '(360) 555-0121', 'visits_this_month': 2, 'last_visit_date': (today - timedelta(days=13)).isoformat(), 'last_visit': {'zipcode': '83843', 'household_size': 3, 'age_0_18': 1, 'age_19_59': 2, 'age_60_plus': 0}},
        {'id': 22, 'first_name': 'Dorothy', 'last_name': 'Hall', 'address': '567 Juniper Street', 'zipcode': '83844', 'phone': '(360) 555-0122', 'visits_this_month': 1, 'last_visit_date': (today - timedelta(days=21)).isoformat(), 'last_visit': {'zipcode': '83844', 'household_size': 1, 'age_0_18': 0, 'age_19_59': 0, 'age_60_plus': 1}},
        {'id': 23, 'first_name': 'Steven', 'last_name': 'Allen', 'address': '890 Sequoia Drive', 'zipcode': '83846', 'phone': '(360) 555-0123', 'visits_this_month': 0, 'last_visit_date': None, 'last_visit': None},
        {'id': 24, 'first_name': 'Carol', 'last_name': 'Young', 'address': '123 Laurel Court', 'zipcode': '83843', 'phone': '(360) 555-0124', 'visits_this_month': 3, 'last_visit_date': (today - timedelta(days=6)).isoformat(), 'last_visit': {'zipcode': '83843', 'household_size': 4, 'age_0_18': 2, 'age_19_59': 2, 'age_60_plus': 0}},
        {'id': 25, 'first_name': 'Paul', 'last_name': 'King', 'address': '456 Fir Avenue', 'zipcode': '83845', 'phone': '(360) 555-0125', 'visits_this_month': 1, 'last_visit_date': (today - timedelta(days=16)).isoformat(), 'last_visit': {'zipcode': '83845', 'household_size': 2, 'age_0_18': 1, 'age_19_59': 1, 'age_60_plus': 0}},
        {'id': 26, 'first_name': 'Margaret', 'last_name': 'Wright', 'address': '789 Cypress Road', 'zipcode': '83844', 'phone': '(360) 555-0126', 'visits_this_month': 2, 'last_visit_date': (today - timedelta(days=10)).isoformat(), 'last_visit': {'zipcode': '83844', 'household_size': 3, 'age_0_18': 0, 'age_19_59': 2, 'age_60_plus': 1}},
        {'id': 27, 'first_name': 'George', 'last_name': 'Lopez', 'address': '321 Alder Place', 'zipcode': '83843', 'phone': '(360) 555-0127', 'visits_this_month': 1, 'last_visit_date': (today - timedelta(days=24)).isoformat(), 'last_visit': {'zipcode': '83843', 'household_size': 5, 'age_0_18': 3, 'age_19_59': 2, 'age_60_plus': 0}},
        {'id': 28, 'first_name': 'Ruth', 'last_name': 'Hill', 'address': '654 Basswood Way', 'zipcode': '83846', 'phone': '(360) 555-0128', 'visits_this_month': 0, 'last_visit_date': None, 'last_visit': None},
        {'id': 29, 'first_name': 'Kenneth', 'last_name': 'Scott', 'address': '987 Locust Lane', 'zipcode': '83845', 'phone': '(360) 555-0129', 'visits_this_month': 2, 'last_visit_date': (today - timedelta(days=12)).isoformat(), 'last_visit': {'zipcode': '83845', 'household_size': 2, 'age_0_18': 0, 'age_19_59': 2, 'age_60_plus': 0}},
        {'id': 30, 'first_name': 'Sharon', 'last_name': 'Green', 'address': '147 Buckeye Street', 'zipcode': '83843', 'phone': '(360) 555-0130', 'visits_this_month': 3, 'last_visit_date': (today - timedelta(days=5)).isoformat(), 'last_visit': {'zipcode': '83843', 'household_size': 4, 'age_0_18': 1, 'age_19_59': 2, 'age_60_plus': 1}},
        
        # Patrons with similar last names for testing partial matching
        {'id': 31, 'first_name': 'Jessica', 'last_name': 'Smith', 'address': '258 Hawthorn Drive', 'zipcode': '83844', 'phone': '(360) 555-0131', 'visits_this_month': 1, 'last_visit_date': (today - timedelta(days=23)).isoformat(), 'last_visit': {'zipcode': '83844', 'household_size': 3, 'age_0_18': 2, 'age_19_59': 1, 'age_60_plus': 0}},
        {'id': 32, 'first_name': 'Ryan', 'last_name': 'Smith', 'address': '369 Blackwood Court', 'zipcode': '83843', 'phone': '(360) 555-0132', 'visits_this_month': 2, 'last_visit_date': (today - timedelta(days=8)).isoformat(), 'last_visit': {'zipcode': '83843', 'household_size': 1, 'age_0_18': 0, 'age_19_59': 1, 'age_60_plus': 0}},
        {'id': 33, 'first_name': 'Amanda', 'last_name': 'Johnson', 'address': '741 Mulberry Avenue', 'zipcode': '83846', 'phone': '(360) 555-0133', 'visits_this_month': 1, 'last_visit_date': (today - timedelta(days=19)).isoformat(), 'last_visit': {'zipcode': '83846', 'household_size': 4, 'age_0_18': 2, 'age_19_59': 2, 'age_60_plus': 0}},
        {'id': 34, 'first_name': 'Brandon', 'last_name': 'Adams', 'address': '852 Ironwood Road', 'zipcode': '83845', 'phone': '(360) 555-0134', 'visits_this_month': 0, 'last_visit_date': None, 'last_visit': None},
        {'id': 35, 'first_name': 'Stephanie', 'last_name': 'Baker', 'address': '963 Pecan Place', 'zipcode': '83843', 'phone': '(360) 555-0135', 'visits_this_month': 2, 'last_visit_date': (today - timedelta(days=14)).isoformat(), 'last_visit': {'zipcode': '83843', 'household_size': 2, 'age_0_18': 1, 'age_19_59': 1, 'age_60_plus': 0}},
        {'id': 36, 'first_name': 'Nicholas', 'last_name': 'Gonzalez', 'address': '159 Rosewood Lane', 'zipcode': '83844', 'phone': '(360) 555-0136', 'visits_this_month': 3, 'last_visit_date': (today - timedelta(days=7)).isoformat(), 'last_visit': {'zipcode': '83844', 'household_size': 5, 'age_0_18': 3, 'age_19_59': 2, 'age_60_plus': 0}},
        {'id': 37, 'first_name': 'Deborah', 'last_name': 'Nelson', 'address': '246 Sassafras Drive', 'zipcode': '83843', 'phone': '(360) 555-0137', 'visits_this_month': 1, 'last_visit_date': (today - timedelta(days=26)).isoformat(), 'last_visit': {'zipcode': '83843', 'household_size': 3, 'age_0_18': 0, 'age_19_59': 2, 'age_60_plus': 1}},
        {'id': 38, 'first_name': 'Aaron', 'last_name': 'Carter', 'address': '753 Teak Court', 'zipcode': '83846', 'phone': '(360) 555-0138', 'visits_this_month': 4, 'last_visit_date': (today - timedelta(days=1)).isoformat(), 'last_visit': {'zipcode': '83846', 'household_size': 6, 'age_0_18': 3, 'age_19_59': 2, 'age_60_plus': 1}},
        {'id': 39, 'first_name': 'Julie', 'last_name': 'Mitchell', 'address': '135 Applewood Way', 'zipcode': '83845', 'phone': '(360) 555-0139', 'visits_this_month': 2, 'last_visit_date': (today - timedelta(days=11)).isoformat(), 'last_visit': {'zipcode': '83845', 'household_size': 2, 'age_0_18': 0, 'age_19_59': 1, 'age_60_plus': 1}},
        {'id': 40, 'first_name': 'Scott', 'last_name': 'Perez', 'address': '468 Cherry Street', 'zipcode': '83843', 'phone': '(360) 555-0140', 'visits_this_month': 1, 'last_visit_date': (today - timedelta(days=20)).isoformat(), 'last_visit': {'zipcode': '83843', 'household_size': 4, 'age_0_18': 2, 'age_19_59': 2, 'age_60_plus': 0}},
    ]
    
    context = {
        'mock_patrons': json.dumps(mock_patrons),
        'is_demo': True,
    }
    return render(request, 'demo.html', context)


def demo_analytics_page(request):
    """Demo statistics page showing sample data visualizations"""
    return render(request, 'demo_analytics.html')


def about_page(request):
    """About page"""
    return render(request, 'about.html')


def pricing_page(request):
    """Pricing page"""
    return render(request, 'pricing.html')


def donate(request):
    """Donate page for supporting FoodBanked's mission"""
    return render(request, 'donate.html')

def custom_404(request, exception):
    """Custom 404 error handler"""
    return render(request, '404.html', status=404)



# def locations(request):
#     """Public locations map page"""
#     # Get all public foodbanks and organizations with coordinates
#     foodbanks = Foodbank.objects.filter(
#         is_public=True,
#         latitude__isnull=False,
#         longitude__isnull=False
#     ).select_related('organization').values(
#         'id', 'name', 'city', 'state', 'latitude', 'longitude', 
#         'description', 'food_truck_enabled', 'organization__name'
#     )
    
#     organizations = FoodbankOrganization.objects.filter(
#         is_public=True,
#         latitude__isnull=False,
#         longitude__isnull=False
#     ).values(
#         'id', 'name', 'city', 'state', 'latitude', 'longitude', 'description'
#     )
    
#     context = {
#         'foodbanks_json': list(foodbanks),
#         'organizations_json': list(organizations),
#         'total_locations': len(foodbanks) + len(organizations),
#     }
    
#     return render(request, 'locations.html', context)
def locations(request):
    """Public locations map page"""
    import json
    
    # Get all public foodbanks and organizations with coordinates
    foodbanks = Foodbank.objects.filter(
        is_public=True,
        latitude__isnull=False,
        longitude__isnull=False
    ).select_related('organization')
    
    organizations = FoodbankOrganization.objects.filter(
        is_public=True,
        latitude__isnull=False,
        longitude__isnull=False
    )
    
    # Convert to list of dicts manually
    foodbanks_list = []
    for fb in foodbanks:
        foodbanks_list.append({
            'id': fb.id,
            'name': fb.name,
            'city': fb.city,
            'state': fb.state,
            'latitude': float(fb.latitude) if fb.latitude else None,
            'longitude': float(fb.longitude) if fb.longitude else None,
            'description': fb.description,
            'food_truck_enabled': fb.food_truck_enabled,
            'organization__name': fb.organization.name if fb.organization else None,
        })
    
    organizations_list = []
    for org in organizations:
        organizations_list.append({
            'id': org.id,
            'name': org.name,
            'city': org.city,
            'state': org.state,
            'latitude': float(org.latitude) if org.latitude else None,
            'longitude': float(org.longitude) if org.longitude else None,
            'description': org.description,
        })
    
    # Convert to JSON
    foodbanks_json = json.dumps(foodbanks_list)
    organizations_json = json.dumps(organizations_list)
    
    context = {
        'foodbanks_json': foodbanks_json,
        'organizations_json': organizations_json,
        'total_locations': len(foodbanks_list) + len(organizations_list),
    }
    
    return render(request, 'locations.html', context)


def location_search(request):
    """AJAX endpoint for searching locations"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    # Search foodbanks
    foodbanks = Foodbank.objects.filter(
        is_public=True,
        name__icontains=query
    ).values('id', 'name', 'city', 'state')[:5]
    
    # Search organizations
    organizations = FoodbankOrganization.objects.filter(
        is_public=True,
        name__icontains=query
    ).values('id', 'name', 'city', 'state')[:5]
    
    results = []
    
    for fb in foodbanks:
        results.append({
            'type': 'foodbank',
            'id': fb['id'],
            'name': fb['name'],
            'location': f"{fb['city']}, {fb['state']}" if fb['city'] and fb['state'] else 'Location not set'
        })
    
    for org in organizations:
        results.append({
            'type': 'organization',
            'id': org['id'],
            'name': org['name'],
            'location': f"{org['city']}, {org['state']}" if org['city'] and org['state'] else 'Location not set'
        })
    
    return JsonResponse({'results': results})

def location_detail(request, location_type, location_id):
    """Detail page for a specific location"""
    if location_type == 'foodbank':
        location = get_object_or_404(
            Foodbank, 
            id=location_id, 
            is_public=True
        )
        location_kind = 'Food Bank'
    elif location_type == 'organization':
        location = get_object_or_404(
            FoodbankOrganization, 
            id=location_id, 
            is_public=True
        )
        location_kind = 'Organization'
    else:
        from django.http import Http404
        raise Http404("Invalid location type")
    
    context = {
        'location': location,
        'location_type': location_type,
        'location_kind': location_kind,
    }
    
    return render(request, 'location_detail.html', context)