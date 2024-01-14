from django import forms
from .models import CustomUser, Vehicle
from crispy_forms.helper import FormHelper
from django.core.validators import RegexValidator


AlphanumericValidator = RegexValidator(r'^[0-9a-zA-Z ]*$', 'Only alphanumeric characters are allowed.')
AlphaValidator = RegexValidator(r'^[a-zA-Z ]*$', 'Only letters are allowed.')
NumberValidator = RegexValidator(r'^[0-9 ]*$', 'Only numbers are allowed.')
PhoneNumberValidator = RegexValidator(r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3,4}[-\s\.]?[0-9]{4,6}$', 'Not a valid phone number.')
EmailValidator = RegexValidator(r'[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+','Not a valid email address.')

class UserForm(forms.ModelForm):
    """
    Form class for user profile 
    """
   
    last_name = forms.CharField(label='Last Name', min_length=3, max_length= 40, validators=[AlphanumericValidator])   
    DOB = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}),required=True, label="Birthday")
    DL_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}),required=True, label="Driver's License Date")
    email = forms.EmailField(max_length=64, widget=forms.TextInput(attrs={}), required=True)

    class Meta:
        model = CustomUser
        
        fields = [
            'first_name',
            'last_name',
            'email',
            'gender',
            'DOB',
            'DL_date',
            'adr_street',
            'adr_city',
            'adr_zip',
            'adr_country',
            'phone',
            'contactable',
            ]

class VehicleForm(forms.ModelForm):
    """
    Form class for users vehicles 
    """
   
    class Meta:
        model = Vehicle
        
        
        fields = [
            'make',
            'model',
            'type',
            'year',
            'engine',
            'smoking',
            'max_pax',
            'status'
            ]

    def __init__(self, *args, **kwargs):
        super(VehicleForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            # Set initial values for vehicle fields
            self.fields['smoking'].initial = instance.smoking
            self.fields['status'].initial = instance.status

    
            
