from django import forms
from .models import CustomUser, Vehicle, Trip, Region, Hitch_Request, Message, Location
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import timedelta, datetime
import re


AlphanumericValidator = RegexValidator(r'^[0-9a-zA-Z ]*$', 'Only alphanumeric characters are allowed.')
AlphaValidator = RegexValidator(r'^[a-zA-Z ]*$', 'Only letters are allowed.')
NumberValidator = RegexValidator(r'^[0-9 ]*$', 'Only numbers are allowed.')
PhoneNumberValidator = RegexValidator(r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3,4}[-\s\.]?[0-9]{4,6}$', 'Not a valid phone number.')
EmailValidator = RegexValidator(r'[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+','Not a valid email address.')
TimeValidator = RegexValidator(r'[^(?:[01]?\d|2[0-3])(?::[0-5]\d){1,2}$]+','Not a valid time.')

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
        # Set initial values for vehicle fields
        if instance is not None:
            self.fields['smoking'].initial = instance.smoking
            self.fields['status'].initial = instance.status

    
class TripForm(forms.ModelForm):
    """
    Form class for offered rides 
    """
    DEPART_WINDOW_CHOICES = [
        (0, 'On Time'),
        (300, '5min'), 
        (600, '10min'),
        (900, '15min'),
        (1800, '30min'),
    ]    

    PICKUP_RADIUS_CHOICES = [
        (0, '2km'),
        (3, '3km'), 
        (5, '5km'),
        (10, '10km'),
        (30, '30km'),
    ]
   

    class DurationInput(forms.TextInput):
        input_type = 'text'    

    depart_window = forms.ChoiceField(choices=DEPART_WINDOW_CHOICES, required=False)
    pickup_radius = forms.ChoiceField(choices=PICKUP_RADIUS_CHOICES, required=False)
    depart_date= forms.DateField(widget=forms.DateInput(attrs={'type': 'date'} ))
    depart_time= forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'} ))
    expected_duration = forms.CharField(widget=DurationInput(attrs={'placeholder': 'H:MM'}), required=False)
    return_time= forms.TimeField(widget=forms.DateInput(attrs={'type': 'time'} ), required=False)

    # def clean(self):
    #     cleaned_data = super().clean()
    #     # Exclude 'driver' from validation
    #     cleaned_data.pop('driver', None)
    #     return cleaned_data
    
    # def clean_expected_duration(self):
    #     duration = self.cleaned_data.get('expected_duration')
    #     if duration == "":
    #         return None
    #     return duration

    class Meta:
        model = Trip
        fields ='__all__'
        exclude = ('driver',)
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TripForm, self).__init__(*args, **kwargs)
        
        if user is not None:
            default_depart_time = (datetime.now() + timedelta(hours=1.5)).strftime('%H:%M')
            default_depart_date = (datetime.now())
            self.fields['vehicle'].queryset = Vehicle.objects.filter(owner=user).order_by('make')
            self.fields['vehicle'].initial = Vehicle.objects.first()
            self.fields['depart'].queryset = Location.objects.filter(input_by=user).order_by('name')
            self.fields['destination'].queryset = Location.objects.filter(input_by=user).order_by('name')
            self.fields['region'].initial = Region.objects.first()
            self.fields['region'].label = False
            self.fields['depart_time'].initial = default_depart_time
            self.fields['depart_date'].initial = default_depart_date
            self.fields['depart_window'].initial = 300
               

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
  
    


class RegionFilterForm(forms.Form):
    selected_region = forms.ModelChoiceField(queryset=Region.objects.all(), empty_label=None, initial=Region.objects.first())
    print(f'Form {selected_region}')
    
    class Meta:
        model = Region
        fields = ['region']

    def __init__(self, *args, **kwargs):
        super(RegionFilterForm, self).__init__(*args, **kwargs)
        self.fields['selected_region'].label = ''
        self.fields['selected_region'].queryset = Region.objects.all()
        self.fields['selected_region'].empty_label = None
        self.fields['selected_region'].initial = Region.objects.first()
        self.fields['selected_region'].widget.attrs.update(style='max-width: 12em')



class MessageForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        max_length=400,
        required=True,)

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        
       
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Div(
                Div('message', css_class='col-md-12'),
                css_class='row'
            ),
        )

    class Meta:
        model = Message
        fields = ['message']
  

class LocationForm(forms.ModelForm):
    """
    Form class for users vehicles 
    """
    helper = FormHelper()
    helper.layout = Layout(
        Div(
                Div('name', css_class='col-md-6'),
                Div('stoptype', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div('street', css_class='col-md-12'),
                css_class='row'
            ),
            Div(
                Div('zipcode', css_class='col-md-6'),
                Div('city', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div('country', css_class='col-md-6'),
                Div('note', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div('region', css_class='col-md-6'),
                css_class='row'
            ),
        )

    class Meta:
        model = Location
        
        
        fields = [
            'name',
            'stoptype',
            'street',
            'zipcode',
            'city',
            'country',
            'note',
            'region'
            ]

    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
 