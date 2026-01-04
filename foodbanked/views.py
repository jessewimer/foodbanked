from django.shortcuts import render
import json

def landing_page(request):
    """Public landing page view"""
    return render(request, 'landing.html')

def demo_page(request):
    """Interactive demo page where users can try the app without logging in"""
    # Mock data for demo with addresses
    mock_patrons = [
        {'id': 1, 'name': 'John Smith', 'address': '123 Main St', 'zipcode': '83843'},
        {'id': 2, 'name': 'Sarah Johnson', 'address': '456 Oak Avenue', 'zipcode': '83844'},
        {'id': 3, 'name': 'Michael Brown', 'address': '789 Pine Road', 'zipcode': '83843'},
        {'id': 4, 'name': 'Emily Davis', 'address': '321 Elm Street', 'zipcode': '83845'},
        {'id': 5, 'name': 'David Wilson', 'address': '654 Maple Drive', 'zipcode': '83843'},
        {'id': 6, 'name': 'Maria Garcia', 'address': '987 Cedar Lane', 'zipcode': '83844'},
        {'id': 7, 'name': 'James Martinez', 'address': '147 Birch Court', 'zipcode': '83846'},
        {'id': 8, 'name': 'Lisa Anderson', 'address': '258 Spruce Way', 'zipcode': '83843'},
        {'id': 9, 'name': 'Robert Taylor', 'address': '369 Willow Path', 'zipcode': '83844'},
        {'id': 10, 'name': 'Jennifer Thomas', 'address': '741 Aspen Boulevard', 'zipcode': '83845'},
        {'id': 11, 'name': 'William Moore', 'address': '852 Hickory Street', 'zipcode': '83843'},
        {'id': 12, 'name': 'Patricia Jackson', 'address': '963 Poplar Avenue', 'zipcode': '83846'},
    ]
    
    context = {
        'mock_patrons': json.dumps(mock_patrons),
        'is_demo': True,
    }
    return render(request, 'demo.html', context)

def demo_stats_page(request):
    """Demo statistics page showing sample data visualizations"""
    return render(request, 'demo_stats.html')