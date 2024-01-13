from django import forms
from .models import CustomUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, ButtonHolder, Column, Fieldset
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class UserForm(forms.ModelForm):
    """
    Form class for user profile 
    """
          
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
 
