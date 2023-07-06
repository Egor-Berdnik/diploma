from django import forms


class WallForm(forms.Form):
    width = forms.IntegerField()
    height = forms.IntegerField()
    cost_of_material = forms.IntegerField()
