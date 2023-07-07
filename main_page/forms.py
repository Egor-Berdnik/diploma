from django import forms
from .models import *


class WallForm(forms.Form):
    width = forms.FloatField()
    height = forms.FloatField()
    cost_of_material = forms.ModelChoiceField\
        (queryset=Materials.objects.values_list('cost', flat=True),
         empty_label='Price is not chosen')
