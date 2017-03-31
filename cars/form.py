from django import forms
import datetime
from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})
class bookingForm(forms.Form):
    start_date = forms.DateField(label="Start Date:", widget=DateInput())

    end_date = forms.DateField(label="End Date", widget=DateInput())


class dateForm(forms.Form):
    start_date = forms.DateField(label="Start Date:", widget=DateInput())