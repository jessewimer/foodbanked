from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def dashboard(request):
    """Main dashboard after login"""
    # Get some basic stats for the dashboard
    context = {
        'foodbank': request.user.foodbank if hasattr(request.user, 'foodbank') else None,
    }
    return render(request, 'accounts/dashboard.html', context)