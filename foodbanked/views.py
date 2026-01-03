from django.shortcuts import render

def landing_page(request):
    """Public landing page view"""
    return render(request, 'landing.html')

def demo_page(request):
    """Interactive demo page where users can try the app without logging in"""
    # Mock data for demo
    mock_patrons = [
        {'id': 1, 'name': 'John Smith', 'zipcode': '83843'},
        {'id': 2, 'name': 'Sarah Johnson', 'zipcode': '83844'},
        {'id': 3, 'name': 'Michael Brown', 'zipcode': '83843'},
        {'id': 4, 'name': 'Emily Davis', 'zipcode': '83845'},
        {'id': 5, 'name': 'David Wilson', 'zipcode': '83843'},
    ]
    
    context = {
        'mock_patrons': mock_patrons,
        'is_demo': True,
    }
    return render(request, 'demo.html', context)