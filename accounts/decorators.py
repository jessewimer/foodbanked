from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.contrib import messages

def is_organization_admin(user):
    """Check if user is an organization admin"""
    if not user.is_authenticated:
        return False
    return hasattr(user, 'organizationadmin')

def is_foodbank_user(user):
    """Check if user is a regular foodbank/pantry user"""
    if not user.is_authenticated:
        return False
    return hasattr(user, 'foodbank')

def organization_required(view_func):
    """
    Decorator for views that require organization admin access.
    Redirects foodbank users to their dashboard with an error message.
    """
    def check_organization(user):
        if not user.is_authenticated:
            return False
        if hasattr(user, 'organizationadmin'):
            return True
        return False
    
    decorated_view = user_passes_test(
        check_organization,
        login_url='/accounts/login/',
        redirect_field_name=None
    )(view_func)
    
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, 'foodbank'):
            # Redirect foodbank users away with a message
            messages.error(request, 'You do not have permission to access organization pages.')
            return redirect('accounts:dashboard')
        return decorated_view(request, *args, **kwargs)
    
    return wrapper

def foodbank_required(view_func):
    """
    Decorator for views that require foodbank/pantry access.
    Redirects organization admins to their dashboard with an error message.
    """
    def check_foodbank(user):
        if not user.is_authenticated:
            return False
        if hasattr(user, 'foodbank'):
            return True
        return False
    
    decorated_view = user_passes_test(
        check_foodbank,
        login_url='/accounts/login/',
        redirect_field_name=None
    )(view_func)
    
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, 'organizationadmin'):
            # Redirect org admins away with a message
            messages.error(request, 'You do not have permission to access foodbank pages.')
            org_slug = request.user.organizationadmin.organization.slug
            return redirect('accounts:organization_dashboard', org_slug=org_slug)
        return decorated_view(request, *args, **kwargs)
    
    return wrapper