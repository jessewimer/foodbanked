from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .forms import FoodbankRegistrationForm


from django.contrib.auth import logout as auth_logout

def logout_view(request):
    """Custom logout view that accepts GET requests"""
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('landing')


def register(request):
    """User registration view with registration code validation"""
    if request.method == 'POST':
        form = FoodbankRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to FoodBanked, {user.foodbank.name}!')
            return redirect('dashboard')
    else:
        form = FoodbankRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def dashboard(request):
    """Main dashboard after login with real statistics"""
    # Import Visit and Patron models
    from visits.models import Visit, Patron
    
    # Get the foodbank
    foodbank = request.user.foodbank if hasattr(request.user, 'foodbank') else None
    
    if not foodbank:
        messages.warning(request, 'No food bank associated with your account.')
        return render(request, 'accounts/dashboard.html', {'foodbank': None})
    
    # Calculate date ranges
    today = timezone.now().date()
    week_start = today - timedelta(days=today.weekday())  # Monday of this week
    month_start = today.replace(day=1)
    
    # Get statistics
    visits_today = Visit.objects.filter(
        foodbank=foodbank,
        visit_date=today
    ).count()
    
    visits_this_week = Visit.objects.filter(
        foodbank=foodbank,
        visit_date__gte=week_start
    ).count()
    
    visits_this_month = Visit.objects.filter(
        foodbank=foodbank,
        visit_date__gte=month_start
    ).count()
    
    total_patrons = Patron.objects.filter(
        foodbank=foodbank
    ).count()
    
    # Get recent visits (last 5)
    recent_visits = Visit.objects.filter(
        foodbank=foodbank
    ).select_related('patron').order_by('-visit_date')[:5]
    
    context = {
        'foodbank': foodbank,
        'visits_today': visits_today,
        'visits_this_week': visits_this_week,
        'visits_this_month': visits_this_month,
        'total_patrons': total_patrons,
        'recent_visits': recent_visits,
    }
    
    return render(request, 'accounts/dashboard.html', context)