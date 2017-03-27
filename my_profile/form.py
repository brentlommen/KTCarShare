from django import forms
from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})
class dropOffForm(forms.Form):
    dropOffDate = forms.DateField(label="Drop Off Date:", widget=DateInput())
    dropOffOdometer = forms.IntegerField(label="Drop Off Odometer:")
    dropOffStatus = forms.CharField(label="Drop Off Status")