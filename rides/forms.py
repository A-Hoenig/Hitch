from django import forms
from .models import CustomUser, Vehicle, Trip, Region, Hitch_Request, Message
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div
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
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Update Data', css_class='btn btn-primary mt-3'))
    helper.form_method = 'POST'
    
    helper.layout = Layout(
        Div(
                Div('first_name', css_class='col-md-6'),
                Div('last_name', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div('email', css_class='col-md-6'),
                Div('gender', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div('DOB', css_class='col-md-6'),
                Div('DL_date', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div('adr_street', css_class='col-md-12'),
                css_class='row'
            ),
            Div(
                Div('adr_zip', css_class='col-md-4'),
                Div('adr_city', css_class='col-md-4'),
                Div('adr_country', css_class='col-md-4'),
                css_class='row'
            ),
            Div(
                Div('phone', css_class='col-md-6'),
                Div('contactable', css_class='col-md-6'),
                css_class='row'
            ),
                         
        )
    
    last_name = forms.CharField(label='Last Name', min_length=3, max_length= 40, validators=[AlphanumericValidator])   
    DOB = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}),required=True, label="Birthday")
    DL_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}),required=True, label="Driver's License Date")
    email = forms.EmailField(max_length=64, widget=forms.TextInput(attrs={'readonly':'readonly'}), required=True)

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
    helper = FormHelper()
    helper.layout = Layout(
        Div(
                Div('make', css_class='col-md-6'),
                Div('model', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div('type', css_class='col-md-6'),
                Div('year', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div('engine', css_class='col-md-6'),
                Div('max_pax', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div('smoking', css_class='col-md-6'),
                Div('status', css_class='col-md-6'),
                css_class='row'
            ),
        )

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

    
class TripForm(forms.ModelForm):
    """
    Form class for offered rides 
    """
    helper = FormHelper()
    helper.form_method = 'POST'
    
    helper.layout = Layout(
        Div(
                Div('region', css_class='dropdown'),
                Div('driver', css_class='col-md-6'),
                Div('trip_date', css_class='col-md-6'),
                css_class='row'
            ),
            
        )

    class Meta:
        model = Trip
        
        fields ='__all__'

    def __init__(self, *args, **kwargs):
        super(TripForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        self.fields['expected_duration'].widget = forms.TimeInput(format='%H:%M')
        self.fields['depart_window'].widget = forms.TimeInput(format='%H:%M')


class HitchRequestForm(forms.ModelForm):
    """
    Form class for ride requests (hitches)
    """
    helper = FormHelper()
    helper.form_method = 'POST'
    
    helper.layout = Layout(
        Div(
                Div('region', css_class='dropdown'),
                Div('hitcher', css_class='col-md-6'),
                Div('depart_date', css_class='col-md-6'),
                css_class='row'
            ),
            
        )

    class Meta:
        model = Hitch_Request
        
        fields ='__all__'

    # def __init__(self, *args, **kwargs):
    #     super(RequestForm, self).__init__(*args, **kwargs)
    #     instance = kwargs.get('instance')
    #     self.fields['expected_duration'].widget = forms.TimeInput(format='%H:%M')
    #     self.fields['depart_window'].widget = forms.TimeInput(format='%H:%M')
   

class RegionFilterForm(forms.Form):
    selected_region = forms.ModelChoiceField(queryset=Region.objects.all(), empty_label=None, initial=Region.objects.first())

    def __init__(self, *args, **kwargs):
        super(RegionFilterForm, self).__init__(*args, **kwargs)
        self.fields['selected_region'].label = ''
        self.fields['selected_region'].queryset = Region.objects.all()
        self.fields['selected_region'].empty_label = None
        self.fields['selected_region'].initial = Region.objects.first()
        self.fields['selected_region'].widget.attrs.update(style='max-width: 12em')

class MessageForm(forms.Form):
    
    class Meta:
        model = Message