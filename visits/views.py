from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Visit, Patron
from .forms import VisitForm


@login_required
def visit_list(request):
    """List all visits for this foodbank"""
    foodbank = request.user.foodbank
    visits = Visit.objects.filter(foodbank=foodbank).order_by('-visit_date')
    
    context = {
        'visits': visits,
    }
    return render(request, 'visits/visit_list.html', context)


@login_required
def visit_create(request):
    """Create a new visit"""
    foodbank = request.user.foodbank
    
    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.foodbank = foodbank
            
            # Check if patron was selected
            patron_id = request.POST.get('patron_id')
            if patron_id:
                try:
                    patron = Patron.objects.get(id=patron_id, foodbank=foodbank)
                    visit.patron = patron
                except Patron.DoesNotExist:
                    pass
            
            visit.save()
            messages.success(request, 'Visit recorded successfully!')
            return redirect('visits:visit_create')  # Stay on same page
    else:
        form = VisitForm()
    
    # Get all patrons for autocomplete
    patrons = Patron.objects.filter(foodbank=foodbank).values('id', 'name', 'address', 'zipcode')
    
    # Get recent visits (last 10)
    recent_visits = Visit.objects.filter(
        foodbank=foodbank
    ).select_related('patron').order_by('-visit_date', '-id')[:10]
    
    context = {
        'form': form,
        'patrons': list(patrons),
        'recent_visits': recent_visits,
    }
    return render(request, 'visits/visit_form.html', context)


@login_required
def visit_detail(request, pk):
    """View/Edit details of a specific visit"""
    foodbank = request.user.foodbank
    visit = get_object_or_404(Visit, pk=pk, foodbank=foodbank)
    
    # Check if we're in edit mode
    edit_mode = request.GET.get('edit') == 'true' or request.method == 'POST'
    
    if request.method == 'POST':
        form = VisitForm(request.POST, instance=visit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Visit updated successfully!')
            return redirect('visits:visit_detail', pk=pk)
    else:
        form = VisitForm(instance=visit) if edit_mode else None
    
    context = {
        'visit': visit,
        'form': form,
        'edit_mode': edit_mode,
    }
    return render(request, 'visits/visit_detail.html', context)


@login_required
def visit_edit(request, pk):
    """Edit an existing visit"""
    foodbank = request.user.foodbank
    visit = get_object_or_404(Visit, pk=pk, foodbank=foodbank)
    
    if request.method == 'POST':
        form = VisitForm(request.POST, instance=visit)
        if form.is_valid():
            # Check if patron was selected
            patron_id = request.POST.get('patron_id')
            if patron_id:
                try:
                    patron = Patron.objects.get(id=patron_id, foodbank=foodbank)
                    visit.patron = patron
                except Patron.DoesNotExist:
                    visit.patron = None
            else:
                visit.patron = None
            
            form.save()
            messages.success(request, 'Visit updated successfully!')
            return redirect('visits:visit_detail', pk=pk)
    else:
        form = VisitForm(instance=visit)
    
    # Get all patrons for autocomplete
    patrons = Patron.objects.filter(foodbank=foodbank).values('id', 'name', 'address', 'zipcode')
    
    context = {
        'form': form,
        'visit': visit,
        'patrons': list(patrons),
    }
    return render(request, 'visits/visit_edit.html', context)


@login_required
def visit_delete(request, pk):
    """Delete a visit"""
    foodbank = request.user.foodbank
    visit = get_object_or_404(Visit, pk=pk, foodbank=foodbank)
    
    if request.method == 'POST':
        visit.delete()
        messages.success(request, 'Visit deleted successfully!')
        return redirect('visits:visit_create')
    
    # If GET request, show confirmation page
    return render(request, 'visits/visit_confirm_delete.html', {'visit': visit})


@login_required
def patron_list(request):
    """List all patrons for this foodbank"""
    foodbank = request.user.foodbank
    patrons = Patron.objects.filter(foodbank=foodbank).order_by('name')
    
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
    visits = Visit.objects.filter(patron=patron).order_by('-visit_date')
    
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