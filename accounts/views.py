from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .forms import FoodbankRegistrationForm
from django.contrib.auth import logout as auth_logout
from .models import ServiceZipcode
from django.http import JsonResponse
from foodbanked.utils import get_foodbank_today
from django.views.decorators.http import require_POST
import json

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
    """Smart dashboard that routes based on account type"""
    
    # Check if they're an organization admin
    if hasattr(request.user, 'organizationadmin'):
        return redirect('organization_dashboard')
    
    # Check if they're a regular foodbank
    elif hasattr(request.user, 'foodbank'):
        return foodbank_dashboard(request)
    
    # Fallback for accounts without proper setup
    else:
        messages.warning(request, 'No food bank or organization associated with your account.')
        return render(request, 'accounts/dashboard.html', {'foodbank': None})


@login_required
def foodbank_dashboard(request):
    """Dashboard for individual foodbanks"""
    # Import Visit and Patron models
    from visits.models import Visit, Patron
    
    # Get the foodbank
    foodbank = request.user.foodbank
    
    # Calculate date ranges
    today = get_foodbank_today(foodbank)
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


@login_required
def organization_dashboard(request):
    """Dashboard for organization admins"""
    from visits.models import Visit, Patron
    
    # Get the organization admin and their organization
    org_admin = request.user.organizationadmin
    organization = org_admin.organization
    
    # Get all member foodbanks
    member_foodbanks = organization.member_foodbanks.all()
    
    # Calculate date ranges (using first foodbank's timezone, or default)
    first_foodbank = member_foodbanks.first()
    if first_foodbank:
        today = get_foodbank_today(first_foodbank)
    else:
        from django.utils import timezone as django_tz
        today = django_tz.now().date()
    
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)
    
    # Aggregate statistics across all member foodbanks
    total_visits_today = Visit.objects.filter(
        foodbank__organization=organization,
        visit_date=today
    ).count()
    
    total_visits_week = Visit.objects.filter(
        foodbank__organization=organization,
        visit_date__gte=week_start
    ).count()
    
    total_visits_month = Visit.objects.filter(
        foodbank__organization=organization,
        visit_date__gte=month_start
    ).count()
    
    total_patrons = Patron.objects.filter(
        foodbank__organization=organization
    ).count()
    
    # Get recent visits across all member foodbanks (last 10)
    recent_visits = Visit.objects.filter(
        foodbank__organization=organization
    ).select_related('patron', 'foodbank').order_by('-visit_date', '-created_at')[:10]
    
    # Statistics by foodbank
    foodbank_stats = []
    for fb in member_foodbanks:
        visits_today = Visit.objects.filter(foodbank=fb, visit_date=today).count()
        visits_month = Visit.objects.filter(foodbank=fb, visit_date__gte=month_start).count()
        foodbank_stats.append({
            'foodbank': fb,
            'visits_today': visits_today,
            'visits_month': visits_month,
        })
    
    context = {
        'organization': organization,
        'member_foodbanks': member_foodbanks,
        'total_visits_today': total_visits_today,
        'total_visits_week': total_visits_week,
        'total_visits_month': total_visits_month,
        'total_patrons': total_patrons,
        'recent_visits': recent_visits,
        'foodbank_stats': foodbank_stats,
    }
    
    return render(request, 'accounts/organization_dashboard.html', context)






# @login_required
# def dashboard(request):
#     """Main dashboard after login with real statistics"""
#     # Import Visit and Patron models
#     from visits.models import Visit, Patron
    
#     # Get the foodbank
#     foodbank = request.user.foodbank if hasattr(request.user, 'foodbank') else None
    
#     if not foodbank:
#         messages.warning(request, 'No food bank associated with your account.')
#         return render(request, 'accounts/dashboard.html', {'foodbank': None})
    
#     # Calculate date ranges
#     today = get_foodbank_today(foodbank)
#     week_start = today - timedelta(days=today.weekday())  # Monday of this week
#     month_start = today.replace(day=1)
    
#     # Get statistics
#     visits_today = Visit.objects.filter(
#         foodbank=foodbank,
#         visit_date=today
#     ).count()
    
#     visits_this_week = Visit.objects.filter(
#         foodbank=foodbank,
#         visit_date__gte=week_start
#     ).count()
    
#     visits_this_month = Visit.objects.filter(
#         foodbank=foodbank,
#         visit_date__gte=month_start
#     ).count()
    
#     total_patrons = Patron.objects.filter(
#         foodbank=foodbank
#     ).count()
    
#     # Get recent visits (last 5)
#     recent_visits = Visit.objects.filter(
#         foodbank=foodbank
#     ).select_related('patron').order_by('-visit_date')[:5]
    
#     context = {
#         'foodbank': foodbank,
#         'visits_today': visits_today,
#         'visits_this_week': visits_this_week,
#         'visits_this_month': visits_this_month,
#         'total_patrons': total_patrons,
#         'recent_visits': recent_visits,
#     }
    
#     return render(request, 'accounts/dashboard.html', context)

@login_required
def account_settings(request):
    """Account settings page for managing foodbank information"""
    foodbank = request.user.foodbank
    
    # Check if we're in edit mode
    edit_mode = request.GET.get('edit') == 'true' or request.method == 'POST'
    
    if request.method == 'POST':
        from .forms import FoodbankForm
        form = FoodbankForm(request.POST, instance=foodbank)
        if form.is_valid():
            form.save()
            messages.success(request, 'Food bank information updated successfully!')
            return redirect('accounts:account_settings')
    else:
        from .forms import FoodbankForm
        form = FoodbankForm(instance=foodbank) if edit_mode else None
    
    # Get service area zip codes
    zipcodes = ServiceZipcode.objects.filter(foodbank=foodbank)
    
    context = {
        'foodbank': foodbank,
        'form': form,
        'edit_mode': edit_mode,
        'zipcodes': zipcodes,
    }
    return render(request, 'accounts/account_settings.html', context)


@login_required
def add_zipcode(request):
    """Add a service area zip code"""
    if request.method == 'POST':
        foodbank = request.user.foodbank
        zipcode = request.POST.get('zipcode')
        city = request.POST.get('city')
        state = request.POST.get('state', '').upper()
        
        ServiceZipcode.objects.create(
            foodbank=foodbank,
            zipcode=zipcode,
            city=city,
            state=state
        )
        messages.success(request, f'Zip code {zipcode} added successfully!')
            
    return redirect('accounts:account_settings')


@login_required
def delete_zipcode(request, pk):
    """Delete a service area zip code"""
    foodbank = request.user.foodbank
    zipcode = get_object_or_404(ServiceZipcode, pk=pk, foodbank=foodbank)
    
    if request.method == 'POST':
        zipcode_num = zipcode.zipcode
        zipcode.delete()
        messages.success(request, f'Zip code {zipcode_num} has been deleted.')
    
    return redirect('accounts:account_settings')


@login_required
def toggle_food_truck(request):
    """Toggle food truck mode for the foodbank"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    
    foodbank = request.user.foodbank
    
    try:
        import json
        data = json.loads(request.body)
        enabled = data.get('enabled', False)
        
        foodbank.food_truck_enabled = enabled
        foodbank.save()
        
        return JsonResponse({
            'success': True,
            'enabled': enabled
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })
    


@login_required
@require_POST
def toggle_by_name(request):
    """Toggle allow_by_name setting via AJAX"""
    try:
        data = json.loads(request.body)
        enabled = data.get('enabled', False)
        
        foodbank = request.user.foodbank
        foodbank.allow_by_name = enabled
        foodbank.save()
        
        return JsonResponse({'success': True, 'enabled': enabled})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@login_required
@require_POST
def toggle_anonymous(request):
    """Toggle allow_anonymous setting via AJAX"""
    try:
        data = json.loads(request.body)
        enabled = data.get('enabled', False)
        
        foodbank = request.user.foodbank
        foodbank.allow_anonymous = enabled
        foodbank.save()
        
        return JsonResponse({'success': True, 'enabled': enabled})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    