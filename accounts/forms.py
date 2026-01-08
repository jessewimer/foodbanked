from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from .models import Foodbank, RegistrationCode, ServiceZipcode


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
    
    # Email fields
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com'
        })
    )
    
    email2 = forms.EmailField(
        label='Confirm Email',
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your email'
        })
    )
    
    # Override username field
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
        fields = ['registration_code', 'foodbank_name', 'username', 'email', 'email2', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already registered.')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        email2 = cleaned_data.get('email2')
        
        if email and email2 and email != email2:
            raise forms.ValidationError('Email addresses do not match.')
        
        return cleaned_data
    
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
        user.email = self.cleaned_data['email']
        
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
# class FoodbankRegistrationForm(UserCreationForm):
#     # Registration code field
#     registration_code = forms.CharField(
#         max_length=50,
#         required=True,
#         help_text='Enter the registration code provided to you',
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Enter registration code'
#         })
#     )
    
#     # Foodbank information
#     foodbank_name = forms.CharField(
#         max_length=200,
#         required=True,
#         help_text='Name of your food bank',
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'e.g., Moscow Food Bank'
#         })
#     )
    
#     # Override username and password fields to add Bootstrap classes
#     username = forms.CharField(
#         max_length=150,
#         required=True,
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Choose a username'
#         })
#     )
    
#     password1 = forms.CharField(
#         label='Password',
#         widget=forms.PasswordInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Create a password'
#         })
#     )
    
#     password2 = forms.CharField(
#         label='Confirm Password',
#         widget=forms.PasswordInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Confirm your password'
#         })
#     )
    
#     class Meta:
#         model = User
#         fields = ['registration_code', 'username', 'password1', 'password2', 'foodbank_name']
    
#     def clean_registration_code(self):
#         code = self.cleaned_data.get('registration_code', '').strip()
        
#         # In DEBUG mode, allow "foodbanked" as a valid code
#         if settings.DEBUG and code.lower() == 'foodbanked':
#             return code
        
#         # Check if code exists and is not used
#         try:
#             reg_code = RegistrationCode.objects.get(code=code, is_used=False)
#             return code
#         except RegistrationCode.DoesNotExist:
#             raise forms.ValidationError('Invalid or already used registration code.')
    
#     def save(self, commit=True):
#         user = super().save(commit=False)
        
#         if commit:
#             user.save()
            
#             # Create associated Foodbank
#             foodbank_name = self.cleaned_data.get('foodbank_name')
#             Foodbank.objects.create(
#                 user=user,
#                 name=foodbank_name
#             )
            
#             # Mark registration code as used (unless it's the DEBUG code)
#             code = self.cleaned_data.get('registration_code')
#             if not (settings.DEBUG and code.lower() == 'foodbanked'):
#                 try:
#                     from django.utils import timezone
#                     reg_code = RegistrationCode.objects.get(code=code)
#                     reg_code.is_used = True
#                     reg_code.used_by = user
#                     reg_code.used_date = timezone.now()
#                     reg_code.save()
#                 except RegistrationCode.DoesNotExist:
#                     pass
        
#         return user

class FoodbankForm(forms.ModelForm):
    """Form for editing foodbank information"""
    
    class Meta:
        model = Foodbank
        fields = ['name', 'address', 'city', 'state', 'zipcode', 'phone', 'email']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Food bank name'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Street address',
                'rows': 2
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State (e.g., WA)',
                'maxlength': 2
            }),
            'zipcode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Zip code'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address'
            }),
        }
        labels = {
            'name': 'Food Bank Name',
            'address': 'Address',
            'city': 'City',
            'state': 'State',
            'zipcode': 'Zip Code',
            'phone': 'Phone',
            'email': 'Email',
        }


class ServiceZipcodeForm(forms.ModelForm):
    """Form for adding service area zip codes"""
    
    class Meta:
        model = ServiceZipcode
        fields = ['zipcode', 'city', 'state']
        widgets = {
            'zipcode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Zip code'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State (e.g., WA)',
                'maxlength': 2
            }),
        }
