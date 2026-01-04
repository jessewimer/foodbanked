from django import forms
from .models import Visit, Patron


class VisitForm(forms.ModelForm):
    """Form for recording a new visit"""
    
    # Optional patron selection (for returning patrons)
    patron_id = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput()
    )
    
    class Meta:
        model = Visit
        fields = ['zipcode', 'household_size', 'age_0_17', 'age_18_30', 'age_31_50', 'age_51_plus', 'first_visit_this_month']
        widgets = {
            'zipcode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter zip code',
                'maxlength': '5'
            }),
            'household_size': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '1'
            }),
            'age_0_17': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'value': '0'
            }),
            'age_18_30': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'value': '0'
            }),
            'age_31_50': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'value': '0'
            }),
            'age_51_plus': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'value': '0'
            }),
            'first_visit_this_month': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'zipcode': 'Zip Code',
            'household_size': 'Household Size',
            'age_0_17': '0-17 years',
            'age_18_30': '18-30 years',
            'age_31_50': '31-50 years',
            'age_51_plus': '51+ years',
            'first_visit_this_month': 'First visit this month'
        }
    
    def clean(self):
        cleaned_data = super().clean()
        household_size = cleaned_data.get('household_size', 0)
        age_0_17 = cleaned_data.get('age_0_17', 0)
        age_18_30 = cleaned_data.get('age_18_30', 0)
        age_31_50 = cleaned_data.get('age_31_50', 0)
        age_51_plus = cleaned_data.get('age_51_plus', 0)
        
        total_ages = age_0_17 + age_18_30 + age_31_50 + age_51_plus
        
        if total_ages != household_size:
            raise forms.ValidationError(
                f'Age groups must add up to household size ({household_size}). Currently adds to {total_ages}.'
            )
        
        return cleaned_data
    

class PatronForm(forms.ModelForm):
    """Form for creating and editing patrons"""
    
    class Meta:
        model = Patron
        fields = ['name', 'address', 'zipcode', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First and last name'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Street address (optional)'
            }),
            'zipcode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Zip code',
                'maxlength': '10'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number (optional)'
            }),
        }
        labels = {
            'name': 'Full Name',
            'address': 'Address',
            'zipcode': 'Zip Code',
            'phone': 'Phone Number',
        }