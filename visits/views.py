from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Visit, Patron
from .forms import VisitForm
from foodbanked.utils import get_foodbank_today


@login_required
def visit_list(request):
    """List all visits for this foodbank with filtering"""
    foodbank = request.user.foodbank
    
    # Get filter parameters
    filter_type = request.GET.get('filter', None)
    visit_type_filter = request.GET.get('visit_type', None)
    
    # Base queryset
    visits = Visit.objects.filter(foodbank=foodbank).select_related('patron')
    
    # Apply visit type filter first
    if visit_type_filter == 'pantry':
        visits = visits.filter(is_food_truck=False)
    elif visit_type_filter == 'food_truck':
        visits = visits.filter(is_food_truck=True)
    
    # Apply time-based filters
    from datetime import timedelta
    
    today = get_foodbank_today(foodbank)
    filter_label = None
    
    if filter_type == 'today':
        visits = visits.filter(visit_date=today)
        filter_label = "today"
    elif filter_type == 'week':
        week_start = today - timedelta(days=today.weekday())  # Monday
        visits = visits.filter(visit_date__gte=week_start)
        filter_label = "this week"
    elif filter_type == 'month':
        month_start = today.replace(day=1)
        visits = visits.filter(visit_date__gte=month_start)
        filter_label = "this month"
    elif filter_type == 'ytd':
        year_start = today.replace(month=1, day=1)
        visits = visits.filter(visit_date__gte=year_start)
        filter_label = "year to date"
        
    # Order by most recent first
    visits = visits.order_by('-visit_date', '-id')
    
    context = {
        'visits': visits,
        'filter': filter_type,
        'filter_label': filter_label,
        'visit_type_filter': visit_type_filter,
    }
    return render(request, 'visits/visit_list.html', context)
# @login_required
# def visit_list(request):
#     """List all visits for this foodbank with filtering"""
#     foodbank = request.user.foodbank
    
#     # Get filter parameter
#     filter_type = request.GET.get('filter', None)
    
#     # Base queryset
#     visits = Visit.objects.filter(foodbank=foodbank).select_related('patron')
    
#     # Apply filters
#     from django.utils import timezone
#     from datetime import timedelta
    
#     today = get_foodbank_today(foodbank)
#     filter_label = None
    
#     if filter_type == 'today':
#         visits = visits.filter(visit_date=today)
#         filter_label = "today"
#     elif filter_type == 'week':
#         week_start = today - timedelta(days=today.weekday())  # Monday
#         visits = visits.filter(visit_date__gte=week_start)
#         filter_label = "this week"
#     elif filter_type == 'month':
#         month_start = today.replace(day=1)
#         visits = visits.filter(visit_date__gte=month_start)
#         filter_label = "this month"
#     elif filter_type == 'ytd':
#         year_start = today.replace(month=1, day=1)
#         visits = visits.filter(visit_date__gte=year_start)
#         filter_label = "year to date"
#     elif filter_type == 'pantry':
#         visits = visits.filter(is_food_truck=False)
#         filter_label = "pantry visits"
#     elif filter_type == 'food_truck':
#         visits = visits.filter(is_food_truck=True)
#         filter_label = "food truck visits"
        
#     # Order by most recent first
#     visits = visits.order_by('-visit_date', '-id')
    
#     context = {
#         'visits': visits,
#         'filter': filter_type,
#         'filter_label': filter_label,
#     }
#     return render(request, 'visits/visit_list.html', context)


@login_required
def visit_create(request):
    """Create a new visit with enhanced patron data"""
    foodbank = request.user.foodbank
    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            # Get visit type selections
            pantry_selected = request.POST.get('visit_type_pantry') == 'on'
            food_truck_selected = request.POST.get('visit_type_food_truck') == 'on'
            
            # Validate at least one is selected (if food truck is enabled)
            if foodbank.food_truck_enabled and not pantry_selected and not food_truck_selected:
                messages.error(request, 'Please select at least one visit type.')
                return redirect('visits:visit_create')
            
            # Get patron info
            patron_id = request.POST.get('patron_id')
            patron = None
            if patron_id:
                try:
                    patron = Patron.objects.get(id=patron_id, foodbank=foodbank)
                except Patron.DoesNotExist:
                    pass
            
            # Create visit(s)
            visits_to_create = []
            
            if foodbank.food_truck_enabled:
                # If food truck is enabled, create based on selections
                if pantry_selected:
                    visits_to_create.append(False)  # Pantry visit
                if food_truck_selected:
                    visits_to_create.append(True)   # Food truck visit
            else:
                # If food truck not enabled, create regular pantry visit
                visits_to_create.append(False)
            
            # Create each visit
            for is_food_truck in visits_to_create:
                visit = Visit(
                    foodbank=foodbank,
                    is_food_truck=is_food_truck,
                    zipcode=form.cleaned_data['zipcode'],
                    city=form.cleaned_data.get('city', ''),  # ADD THIS
                    state=form.cleaned_data.get('state', ''),
                    household_size=form.cleaned_data['household_size'],
                    age_0_18=form.cleaned_data['age_0_18'],
                    age_19_59=form.cleaned_data['age_19_59'],
                    age_60_plus=form.cleaned_data['age_60_plus'],
                    first_visit_this_month=form.cleaned_data['first_visit_this_month'],
                    comments=form.cleaned_data.get('comments', ''),
                )
                
                if patron:
                    visit.patron = patron
                    visit.patron_first_name = patron.first_name
                    visit.patron_last_name = patron.last_name
                    visit.patron_address = patron.address
                
                visit.save()




            # Success message
            visit_count = len(visits_to_create)
            if visit_count == 1:
                messages.success(request, 'Visit recorded successfully!')
            else:
                messages.success(request, f'{visit_count} visits recorded successfully!')
            
            return redirect('visits:visit_create')
    else:
        form = VisitForm()

    # Get all patrons with enhanced data for autocomplete
    from django.utils import timezone
    from django.db.models import Count
    import json
    
    today = get_foodbank_today(foodbank)
    month_start = today.replace(day=1)
    
    patrons_queryset = Patron.objects.filter(foodbank=foodbank)
    patrons = []
    
    for patron in patrons_queryset:
        # Get visits this month count
        visits_this_month = Visit.objects.filter(
            patron=patron,
            visit_date__gte=month_start
        ).count()
        
        # Get last visit
        last_visit = Visit.objects.filter(patron=patron).order_by('-visit_date', '-id').first()
        
        patron_data = {
            'id': patron.id,
            'first_name': patron.first_name,
            'last_name': patron.last_name,
            'address': patron.address or '',
            'city': patron.city or '',
            'state': patron.state or '',
            'zipcode': patron.zipcode,
            'phone': patron.phone or '',
            'comments': patron.comments or '',
            'phone': patron.phone or '',
            'visits_this_month': visits_this_month,
        }
        
        # Add last visit data if exists
        if last_visit:
            # patron_data['last_visit_date'] = last_visit.visit_date.isoformat()
            patron_data['last_visit_date'] = last_visit.visit_date.strftime('%Y-%m-%d')
            patron_data['last_visit'] = {
                'zipcode': last_visit.zipcode,
                'household_size': last_visit.household_size,
                'age_0_18': last_visit.age_0_18,
                'age_19_59': last_visit.age_19_59,
                'age_60_plus': last_visit.age_60_plus,
            }
        else:
            patron_data['last_visit_date'] = None
            patron_data['last_visit'] = None
        
        patrons.append(patron_data)
    
    today = get_foodbank_today(foodbank)
    recent_visits = Visit.objects.filter(
        foodbank=foodbank,
        visit_date=today,  # Only show today's visits
        is_food_truck=False 
    ).select_related('patron').order_by('-id')

    # Count today's visits for display
    todays_visit_count = Visit.objects.filter(
        foodbank=foodbank,
        visit_date=today,
        is_food_truck=False 
    ).count()
        
    context = {
        'form': form,
        'patrons': json.dumps(patrons),
        'recent_visits': recent_visits,
        'todays_visit_count': todays_visit_count,
        'food_truck_enabled': foodbank.food_truck_enabled,
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
    """List all patrons for this foodbank with search and filtering"""
    foodbank = request.user.foodbank
    
    # Base queryset
    patrons = Patron.objects.filter(foodbank=foodbank)
    
    # Search functionality (search in both first_name and last_name)
    search_query = request.GET.get('search', '').strip()
    if search_query:
        from django.db.models import Q
        patrons = patrons.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(zipcode__icontains=search_query) |
            Q(phone__icontains=search_query)
        )
    
    # Letter filtering (filter by first letter of LAST name)
    letter_filter = request.GET.get('letter', '').strip().upper()
    if letter_filter and letter_filter.isalpha():
        patrons = patrons.filter(last_name__istartswith=letter_filter)
    
    # Order alphabetically by LAST name, then first name
    patrons = patrons.order_by('last_name', 'first_name')
    
    context = {
        'patrons': patrons,
        'search_query': search_query,
        'letter_filter': letter_filter,
    }
    return render(request, 'visits/patron_list.html', context)


@login_required
def patron_detail(request, pk):
    """View/Edit details of a specific patron"""
    foodbank = request.user.foodbank
    patron = get_object_or_404(Patron, pk=pk, foodbank=foodbank)
    
    # Get visit history for this patron
    visits = Visit.objects.filter(patron=patron).order_by('-visit_date')
    
    # Check if we're in edit mode
    edit_mode = request.GET.get('edit') == 'true' or request.method == 'POST'
    
    if request.method == 'POST':
        from .forms import PatronForm
        form = PatronForm(request.POST, instance=patron)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patron updated successfully!')
            return redirect('visits:patron_detail', pk=pk)
    else:
        from .forms import PatronForm
        form = PatronForm(instance=patron) if edit_mode else None
    
    context = {
        'patron': patron,
        'visits': visits,
        'form': form,
        'edit_mode': edit_mode,
    }
    return render(request, 'visits/patron_detail.html', context)


@login_required
def patron_create(request):
    """Create a new patron"""
    foodbank = request.user.foodbank
    
    if request.method == 'POST':
        from .forms import PatronForm
        form = PatronForm(request.POST)
        if form.is_valid():
            patron = form.save(commit=False)
            patron.foodbank = foodbank
            patron.save()
            messages.success(request, 'Patron added successfully!')
            return redirect('visits:patron_detail', pk=patron.pk)
    else:
        from .forms import PatronForm
        form = PatronForm()
    
    context = {
        'form': form,
    }
    return render(request, 'visits/patron_form.html', context)


@login_required
def patron_delete(request, pk):
    """Delete a patron"""
    foodbank = request.user.foodbank
    patron = get_object_or_404(Patron, pk=pk, foodbank=foodbank)
    
    if request.method == 'POST':
        patron.delete()
        messages.success(request, f'{patron.name} has been deleted.')
        return redirect('visits:patron_list')
    
    # If GET request, redirect to detail page
    return redirect('visits:patron_detail', pk=pk)


@login_required
def stats_view(request):
    """View statistics and reports with real data"""
    foodbank = request.user.foodbank
    
    from django.db.models import Sum, Count, Q
    from django.utils import timezone
    from datetime import timedelta
    import json
    
    today = get_foodbank_today(foodbank)
    month_start = today.replace(day=1)
    thirty_days_ago = today - timedelta(days=30)
    
    # Quick Stats
    visits_this_month = Visit.objects.filter(
        foodbank=foodbank,
        visit_date__gte=month_start
    ).count()
    
    # Unique households this month (count distinct patrons + anonymous visits)
    identified_households = Visit.objects.filter(
        foodbank=foodbank,
        visit_date__gte=month_start,
        patron__isnull=False
    ).values('patron').distinct().count()
    
    anonymous_visits = Visit.objects.filter(
        foodbank=foodbank,
        visit_date__gte=month_start,
        patron__isnull=True
    ).count()
    
    unique_households = identified_households + anonymous_visits
    
    # People served this month (sum of household sizes)
    people_served = Visit.objects.filter(
        foodbank=foodbank,
        visit_date__gte=month_start
    ).aggregate(total=Sum('household_size'))['total'] or 0
    
    # First-time visitors this month
    first_time_visitors = Visit.objects.filter(
        foodbank=foodbank,
        visit_date__gte=month_start,
        first_visit_this_month=True
    ).count()
    
    # Visits Over Time (last 30 days)
    visits_by_date = {}
    for i in range(30):
        date = today - timedelta(days=29-i)
        visits_by_date[date] = 0
    
    visit_counts = Visit.objects.filter(
        foodbank=foodbank,
        visit_date__gte=thirty_days_ago
    ).values('visit_date').annotate(count=Count('id'))
    
    for item in visit_counts:
        visits_by_date[item['visit_date']] = item['count']
    
    visits_over_time = {
        'labels': [date.strftime('%b %d') for date in sorted(visits_by_date.keys())],
        'values': [visits_by_date[date] for date in sorted(visits_by_date.keys())]
    }
    
    # Age Distribution
    age_totals = Visit.objects.filter(
        foodbank=foodbank,
        visit_date__gte=month_start
    ).aggregate(
        age_0_18=Sum('age_0_18'),
        age_19_59=Sum('age_19_59'),
        age_60_plus=Sum('age_60_plus')
    )
    
    age_distribution = {
        'labels': ['0-18 years', '19-59 years', '60+ years'],
        'values': [
            age_totals['age_0_18'] or 0,
            age_totals['age_19_59'] or 0,
            age_totals['age_60_plus'] or 0
        ]
    }
    
    # Top Zip Codes
    zip_codes = Visit.objects.filter(
        foodbank=foodbank,
        visit_date__gte=month_start
    ).values('zipcode').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    max_zip_count = zip_codes[0]['count'] if zip_codes else 1
    zip_code_data = [
        {
            'zipcode': item['zipcode'],
            'count': item['count'],
            'percentage': (item['count'] / max_zip_count * 100) if max_zip_count > 0 else 0
        }
        for item in zip_codes
    ]
    
    # Household Sizes
    household_sizes = Visit.objects.filter(
        foodbank=foodbank,
        visit_date__gte=month_start
    ).values('household_size').annotate(
        count=Count('id')
    ).order_by('household_size')
    
    max_household_count = max([item['count'] for item in household_sizes], default=1)
    household_size_data = [
        {
            'size': item['household_size'],
            'count': item['count'],
            'percentage': (item['count'] / max_household_count * 100) if max_household_count > 0 else 0
        }
        for item in household_sizes
    ]
    
    context = {
        'foodbank': foodbank,
        'visits_this_month': visits_this_month,
        'unique_households': unique_households,
        'people_served': people_served,
        'first_time_visitors': first_time_visitors,
        'visits_over_time': json.dumps(visits_over_time),
        'age_distribution': json.dumps(age_distribution),
        'zip_code_data': zip_code_data,
        'household_size_data': household_size_data,
    }
    
    return render(request, 'visits/stats.html', context)


@login_required
def patron_edit_ajax(request, pk):
    """AJAX endpoint for editing patron details from visit form"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    
    foodbank = request.user.foodbank
    patron = get_object_or_404(Patron, pk=pk, foodbank=foodbank)
    
    try:
        import json
        data = json.loads(request.body)
        
        # Update patron fields
        patron.first_name = data.get('first_name', patron.first_name)
        patron.last_name = data.get('last_name', patron.last_name)
        patron.address = data.get('address', '')
        patron.city = data.get('city', '')
        patron.state = data.get('state', '')
        patron.zipcode = data.get('zipcode', patron.zipcode)
        patron.phone = data.get('phone', '')
        patron.comments = data.get('comments', '')
        
        patron.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Patron updated successfully'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })