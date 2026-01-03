from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Visit, Patron

@login_required
def dashboard(request):
    """Dashboard view - shows quick stats"""
    foodbank = request.user.foodbank
    
    # Get some basic stats
    from django.utils import timezone
    from datetime import timedelta
    
    today = timezone.now().date()
    this_month_start = today.replace(day=1)
    
    visits_today = Visit.objects.filter(
        foodbank=foodbank,
        visit_date=today
    ).count()
    
    visits_this_month = Visit.objects.filter(
        foodbank=foodbank,
        visit_date__gte=this_month_start
    ).count()
    
    context = {
        'visits_today': visits_today,
        'visits_this_month': visits_this_month,
        'foodbank': foodbank,
    }
    return render(request, 'visits/dashboard.html', context)


@login_required
def visit_list(request):
    """List all visits for this foodbank"""
    foodbank = request.user.foodbank
    visits = Visit.objects.filter(foodbank=foodbank)
    
    context = {
        'visits': visits,
    }
    return render(request, 'visits/visit_list.html', context)


@login_required
def visit_create(request):
    """Create a new visit"""
    if request.method == 'POST':
        # Handle form submission
        # TODO: Create form and process
        messages.success(request, 'Visit recorded successfully!')
        return redirect('visits:visit_list')
    
    foodbank = request.user.foodbank
    patrons = Patron.objects.filter(foodbank=foodbank)
    
    context = {
        'patrons': patrons,
    }
    return render(request, 'visits/visit_form.html', context)


@login_required
def visit_detail(request, pk):
    """View details of a specific visit"""
    foodbank = request.user.foodbank
    visit = get_object_or_404(Visit, pk=pk, foodbank=foodbank)
    
    context = {
        'visit': visit,
    }
    return render(request, 'visits/visit_detail.html', context)


@login_required
def patron_list(request):
    """List all patrons for this foodbank"""
    foodbank = request.user.foodbank
    patrons = Patron.objects.filter(foodbank=foodbank)
    
    context = {
        'patrons': patrons,
    }
    return render(request, 'visits/patron_list.html', context)


@login_required
def patron_create(request):
    """Create a new patron"""
    if request.method == 'POST':
        # Handle form submission
        # TODO: Create form and process
        messages.success(request, 'Patron added successfully!')
        return redirect('visits:patron_list')
    
    return render(request, 'visits/patron_form.html')


@login_required
def patron_detail(request, pk):
    """View details of a specific patron and their visit history"""
    foodbank = request.user.foodbank
    patron = get_object_or_404(Patron, pk=pk, foodbank=foodbank)
    visits = Visit.objects.filter(patron=patron)
    
    context = {
        'patron': patron,
        'visits': visits,
    }
    return render(request, 'visits/patron_detail.html', context)


@login_required
def stats_view(request):
    """View statistics and reports"""
    foodbank = request.user.foodbank
    
    # TODO: Add date range filtering and actual stats
    
    context = {
        'foodbank': foodbank,
    }
    return render(request, 'visits/stats.html', context)