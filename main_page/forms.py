from django import forms
from .models import *


class WallForm(forms.Form):
    width = forms.FloatField()
    height = forms.FloatField()
    width_of_door = forms.FloatField(required=False, label="Width of door or window")
    height_of_door = forms.FloatField(required=False, label="Height of door or window")
    cost_of_material = forms.ModelChoiceField\
        (queryset=Materials.objects.values_list('cost', flat=True),
         empty_label='Price is not chosen')
