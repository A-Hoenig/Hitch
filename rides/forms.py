from django import forms
from .models import Region


class RegionForm(forms.ModelForm):
    """
    Form class for users to add a new region 
    """
    class Meta:
        """
        Specify the django model and order of the fields
        """
        model = Region
        fields = ('region',)

