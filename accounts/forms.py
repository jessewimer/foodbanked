from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from .models import Foodbank, RegistrationCode


class FoodbankRegistrationForm(UserCreationForm):
    # Registration code field
    registration_code = forms.CharField(
        max_length=50,
        required=True,
        help_text='Enter the registration code provided to you',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter registration code'
        })
    )
    
    # Foodbank information
    foodbank_name = forms.CharField(
        max_length=200,
        required=True,
        help_text='Name of your food bank',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Moscow Food Bank'
        })
    )
    
    # Override username and password fields to add Bootstrap classes
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
    )
    
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create a password'
        })
    )
    
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
    )
    
    class Meta:
        model = User
        fields = ['registration_code', 'username', 'password1', 'password2', 'foodbank_name']
    
    def clean_registration_code(self):
        code = self.cleaned_data.get('registration_code', '').strip()
        
        # In DEBUG mode, allow "foodbanked" as a valid code
        if settings.DEBUG and code.lower() == 'foodbanked':
            return code
        
        # Check if code exists and is not used
        try:
            reg_code = RegistrationCode.objects.get(code=code, is_used=False)
            return code
        except RegistrationCode.DoesNotExist:
            raise forms.ValidationError('Invalid or already used registration code.')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        if commit:
            user.save()
            
            # Create associated Foodbank
            foodbank_name = self.cleaned_data.get('foodbank_name')
            Foodbank.objects.create(
                user=user,
                name=foodbank_name
            )
            
            # Mark registration code as used (unless it's the DEBUG code)
            code = self.cleaned_data.get('registration_code')
            if not (settings.DEBUG and code.lower() == 'foodbanked'):
                try:
                    from django.utils import timezone
                    reg_code = RegistrationCode.objects.get(code=code)
                    reg_code.is_used = True
                    reg_code.used_by = user
                    reg_code.used_date = timezone.now()
                    reg_code.save()
                except RegistrationCode.DoesNotExist:
                    pass
        
        return user