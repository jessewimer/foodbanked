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
        fields = ['zipcode', 'household_size', 'age_0_18', 'age_19_59', 'age_60_plus', 'first_visit_this_month']
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
            'age_0_18': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'value': '0'
            }),
            'age_19_59': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'value': '0'
            }),

            'age_60_plus': forms.NumberInput(attrs={
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
            'age_0_18': '0-18 years',
            'age_19_59': '19-59 years',
            'age_60_plus': '60+ years',
            'first_visit_this_month': 'First visit this month'
        }
    
    def clean(self):
        cleaned_data = super().clean()
        household_size = cleaned_data.get('household_size', 0)
        age_0_18 = cleaned_data.get('age_0_18', 0)
        age_19_59 = cleaned_data.get('age_19_59', 0)
        age_60_plus = cleaned_data.get('age_60_plus', 0)
        
        total_ages = age_0_18 + age_19_59 + age_60_plus
        
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